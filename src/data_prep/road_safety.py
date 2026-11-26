"""Build and check the shared STATS19 inputs described in question.md."""

from pathlib import Path

import pandas as pd


ACCIDENT_COLUMNS = {
    "Accident_Index": "accident_id",
    "Date": "accident_date",
    "Time": "accident_time",
    "Accident_Severity": "accident_severity",
    "Road_Type": "road_type",
    "Speed_limit": "speed_limit",
    "Urban_or_Rural_Area": "urban_or_rural_area",
    "Light_Conditions": "light_conditions",
    "Road_Surface_Conditions": "road_surface_conditions",
    "Weather_Conditions": "weather_conditions",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Junction_Detail": "junction_detail",
    "Junction_Control": "junction_control",
    "Number_of_Vehicles": "n_vehicles_reported",
}
VEHICLE_COLUMNS = {
    "Accident_Index": "accident_id",
    "Vehicle_Reference": "vehicle_ref",
    "Vehicle_Type": "vehicle_type",
    "1st_Point_of_Impact": "first_point_of_impact",
    "Vehicle_Manoeuvre": "vehicle_manoeuvre",
    "Skidding_and_Overturning": "skidding_and_overturning",
}
CASUALTY_COLUMNS = {
    "Accident_Index": "accident_id",
    "Casualty_Reference": "casualty_ref",
    "Vehicle_Reference": "vehicle_ref",
    "Casualty_Type": "casualty_type",
    "Age_of_Casualty": "age",
    "Age_Band_of_Casualty": "age_band",
    "Casualty_Severity": "casualty_severity",
}
VEHICLE_KEY = ["accident_id", "vehicle_ref"]
CASUALTY_KEY = [*VEHICLE_KEY, "casualty_ref"]


def _read_raw(path, required, *, imd_field, imd_aliases):
    header = pd.read_csv(path, nrows=0).columns
    missing = sorted(set(required) - set(header))
    if missing:
        raise ValueError(f"{path.name} thiếu cột: {', '.join(missing)}")

    columns = dict(required)
    # Các phiên bản lịch sử có thể thiếu trường IMD. Giữ thiếu để báo độ phủ.
    imd_source = next((name for name in imd_aliases if name in header), None)
    if imd_source:
        columns[imd_source] = imd_field

    source_dtypes = {
        "Accident_Index": "string", "Date": "string", "Time": "string",
        "Latitude": "float64", "Longitude": "float64",
    }
    dtypes = {name: source_dtypes.get(name, "Int32") for name in columns}
    # Có bản CSV lịch sử thêm trường cuối dòng mà không khai báo trong tiêu đề.
    frame = pd.read_csv(path, usecols=list(columns), dtype=dtypes, index_col=False)
    frame = frame.rename(columns=columns)
    frame["accident_id"] = frame["accident_id"].str.strip().replace(
        {"": pd.NA, "-1": pd.NA}
    )
    # Longitude = -1 là một tọa độ có thể hợp lệ. Chỉ đổi -1 ở cột mã/số đếm.
    for original, name in columns.items():
        if dtypes[original] == "Int32":
            frame[name] = frame[name].mask(frame[name].eq(-1))

    if not imd_source:
        frame[imd_field] = pd.Series(pd.NA, index=frame.index, dtype="Int32")
    imd = frame[imd_field]
    frame[imd_field] = imd.where(imd.between(1, 10))
    return frame


def _check_unique(frame, keys, label, *, allow_incomplete=False):
    complete = frame[keys].notna().all(axis=1)
    if not allow_incomplete and not complete.all():
        raise ValueError(f"{label} có {int((~complete).sum())} dòng thiếu khóa {keys}.")
    duplicates = frame.loc[complete, keys].duplicated(keep=False).sum()
    if duplicates:
        raise ValueError(f"{label} có {int(duplicates)} dòng trùng khóa {keys}.")


def build_tables(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Return four shared tables while keeping incomplete joins visible."""

    accidents = _read_raw(
        raw_dir / "Accidents0515.csv", ACCIDENT_COLUMNS,
        imd_field="accident_imd_decile", imd_aliases=("Accident_IMD_Decile", "IMD_Decile"),
    )
    vehicles = _read_raw(
        raw_dir / "Vehicles0515.csv", VEHICLE_COLUMNS,
        imd_field="driver_imd_decile", imd_aliases=("Driver_IMD_Decile", "Vehicle_IMD_Decile"),
    )
    casualties = _read_raw(
        raw_dir / "Casualties0515.csv", CASUALTY_COLUMNS,
        imd_field="casualty_imd_decile", imd_aliases=("Casualty_IMD_Decile",),
    )
    _check_unique(accidents, ["accident_id"], "Accidents0515.csv")
    _check_unique(vehicles, VEHICLE_KEY, "Vehicles0515.csv", allow_incomplete=True)
    # Một số vụ tái sử dụng casualty_ref giữa các phương tiện.
    _check_unique(casualties, CASUALTY_KEY, "Casualties0515.csv", allow_incomplete=True)

    accidents["accident_date"] = pd.to_datetime(
        accidents["accident_date"], format="mixed", dayfirst=True, errors="coerce"
    )
    accidents["accident_year"] = accidents["accident_date"].dt.year.astype("Int16")
    accidents["accident_month"] = accidents["accident_date"].dt.month.astype("Int8")
    accidents["accident_weekday"] = accidents["accident_date"].dt.dayofweek.astype("Int8")
    accidents["accident_hour"] = (
        accidents["accident_time"].str.strip()
        .str.extract(r"^([01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$", expand=False)
        .astype("Int8")
    )
    severity = accidents["accident_severity"]
    accidents["is_ksi"] = severity.map({1: True, 2: True, 3: False}).astype("boolean")

    casualty_vehicle = casualties.merge(
        vehicles.dropna(subset=VEHICLE_KEY), on=VEHICLE_KEY,
        how="left", validate="many_to_one", indicator=True,
    )
    match_status = casualty_vehicle.pop("_merge").map(
        {"left_only": "unmatched", "both": "matched", "right_only": "unmatched"}
    )
    casualty_vehicle["vehicle_match_status"] = match_status.where(
        casualty_vehicle[VEHICLE_KEY].notna().all(axis=1), "missing_key"
    ).astype("string")
    casualty_vehicle = casualty_vehicle.merge(
        accidents[["accident_id", "accident_year"]],
        on="accident_id", how="left", validate="many_to_one",
    )
    vehicle_accident = vehicles.merge(
        accidents[["accident_id", "accident_year", "road_type", "speed_limit",
                   "road_surface_conditions", "weather_conditions", "latitude", "is_ksi"]],
        on="accident_id", how="left", validate="many_to_one", indicator="accident_match",
    )

    vehicle_counts = vehicles.groupby("accident_id").size().rename("n_vehicles")
    casualty_counts = casualties.groupby("accident_id").size().rename("n_casualties")
    valid_severity = casualties["casualty_severity"].where(
        casualties["casualty_severity"].isin([1, 2, 3])
    )
    fatal_counts = valid_severity.eq(1).groupby(casualties["accident_id"]).sum(min_count=1)
    known_severity_counts = valid_severity.groupby(casualties["accident_id"]).count()
    counts = pd.concat(
        [vehicle_counts, casualty_counts, fatal_counts.rename("n_fatal_casualties"),
         known_severity_counts.rename("n_casualties_with_severity")],
        axis=1,
    )
    accident_counts = accidents[[
        "accident_id", "accident_date", "accident_year", "accident_severity", "is_ksi",
        "road_type", "speed_limit", "urban_or_rural_area", "accident_imd_decile",
    ]].join(counts, on="accident_id", validate="one_to_one")
    count_columns = ["n_vehicles", "n_casualties", "n_fatal_casualties", "n_casualties_with_severity"]
    accident_counts[count_columns] = accident_counts[count_columns].astype("Int64")

    return {
        "accidents_clean.csv": accidents,
        "casualty_vehicle.csv": casualty_vehicle,
        "vehicle_accident.csv": vehicle_accident,
        "accident_counts.csv": accident_counts,
    }


def preview_table(path: Path, columns: list[str], *, rows: int = 5) -> pd.DataFrame:
    """Read a few rows and report missing columns in a processed table."""

    preview = pd.read_csv(path, nrows=rows, dtype={"accident_id": "string"})
    missing = sorted(set(columns) - set(preview))
    if missing:
        raise ValueError(f"{path.name} thiếu cột: {', '.join(missing)}. Chạy lại notebook 01.")
    return preview[columns]


def read_lookup(path: Path, *, code_column: str, label_column: str) -> pd.Series:
    """Read a codebook after checking the headers of the downloaded context CSV."""

    codes = pd.read_csv(path, usecols=[code_column, label_column], dtype="string")
    keys = codes[code_column].str.strip()
    labels = codes[label_column].str.strip()
    if keys.isna().any() or keys.eq("").any() or keys.duplicated().any():
        raise ValueError(f"{path.name} có mã thiếu hoặc trùng.")
    if labels.isna().any() or labels.eq("").any():
        raise ValueError(f"{path.name} có nhãn thiếu.")
    return pd.Series(labels.array, index=keys, name=label_column)
