# Hướng dẫn thực hiện đồ án CSC17104

Dùng tài liệu này để thiết lập máy, nhận câu hỏi phụ trách, chạy notebook và chuẩn bị bản nộp. Mã câu, mục tiêu và lộ trình nghiên cứu được thống nhất theo [question.md](question.md). [Đề bài chính thức](CSC17104_2026_Final_Project.pdf)

## 1. Thiết lập ban đầu

### Lấy repo

```bash
git clone https://github.com/minhvonhat/Data-Science-Final-Project.git
cd Data-Science-Final-Project
git switch vnhatminh
```

`vnhatminh` là nhánh tích hợp để nhóm làm việc. `main` lưu phiên bản đã thống nhất. Trên Codex Cloud, dùng checkout hiện có tại `/workspace/Data-Science-Final-Project` và kiểm tra nhánh bằng `git branch --show-current`.

### Cài Miniconda và Jupyter Notebook

Cài Miniconda theo hệ điều hành và kiến trúc máy. Trên Windows, chạy lệnh trong **Anaconda Prompt** hoặc **Miniconda Prompt**. Trên macOS/Linux, mở lại terminal sau khi cài. [Bộ cài Miniconda](https://repo.anaconda.com/miniconda/)

```bash
conda --version
conda create -n min_ds-env python=3.11 pip
conda activate min_ds-env
python -m pip install notebook==7.0.8
python -m pip install numpy==1.26.0 pandas==2.1.1 scipy==1.11.3 matplotlib==3.8.0 seaborn==0.13.0 scikit-learn==1.3.1
python --version
jupyter notebook --version
```

Nếu đã có `min_ds-env` với Python 3.11, bắt đầu từ lệnh kích hoạt. Mỗi terminal mới cần kích hoạt lại môi trường. Các phiên bản thư viện theo cấu hình dự án được cài bằng `pip` vì kênh Conda `defaults` thiếu một số phiên bản ghim. [Cấu hình môi trường](environment.yml)

Trên Codex Cloud, nếu checkout đã có `.venv`, dùng `source .venv/bin/activate`. Nếu Jupyter hoặc công cụ vẽ cần thư mục có quyền ghi, chạy các lệnh sau sau khi kích hoạt.

```bash
export JUPYTER_CONFIG_DIR="$VIRTUAL_ENV/jupyter/config"
export JUPYTER_RUNTIME_DIR="$VIRTUAL_ENV/jupyter/runtime"
export IPYTHONDIR="$VIRTUAL_ENV/ipython"
export MPLCONFIGDIR="$VIRTUAL_ENV/cache/matplotlib"
export XDG_CACHE_HOME="$VIRTUAL_ENV/cache"
mkdir -p "$JUPYTER_CONFIG_DIR" "$JUPYTER_RUNTIME_DIR" "$IPYTHONDIR" "$MPLCONFIGDIR"
```

### Chuẩn bị ba CSV

Từ trang Kaggle của `silicon99/dft-accident-data`, tải ba tệp dưới đây. Nếu nhận tệp `.zip`, giải nén để đặt các CSV trực tiếp trong `data/raw/`. Dùng đúng tên và chữ hoa vì Linux phân biệt hoa thường. [Trang tải dữ liệu](https://www.kaggle.com/datasets/silicon99/dft-accident-data?resource=download&select=Vehicles0515.csv)

| Đường dẫn | Đơn vị quan sát | Khóa cần kiểm tra |
| --- | --- | --- |
| `data/raw/Accidents0515.csv` | Một vụ tai nạn | `Accident_Index` |
| `data/raw/Vehicles0515.csv` | Một phương tiện liên quan trong một vụ | `Accident_Index` và `Vehicle_Reference` |
| `data/raw/Casualties0515.csv` | Một người bị nạn trong một vụ | `Accident_Index`, `Vehicle_Reference` và `Casualty_Reference` với khóa đầy đủ. |

Giữ CSV và ZIP lớn trên máy. Quy tắc `.gitignore` trong repo đã bỏ qua dữ liệu ở `data/raw/` và đầu ra sinh lại ở `data/processed/`. Kiểm tra sau khi tải bằng `git status --short --ignored -- data/raw/`. Ký hiệu `!!` cho biết dữ liệu đang được bỏ qua.

Người phụ trách nguồn ghi phiên bản/ngày tải, tên nguồn phát hành, giấy phép và ghi công hiển thị trên phiên bản Kaggle đã dùng. Đối chiếu ngữ nghĩa các cột, mã phân loại và phạm vi bao phủ với tài liệu STATS19 của Department for Transport. Giấy phép trong repo áp dụng cho phần do nhóm có quyền cấp phép. Dữ liệu gốc tuân theo điều khoản của nguồn phát hành. [Nguồn Kaggle](https://www.kaggle.com/datasets/silicon99/dft-accident-data) · [Tài liệu và dữ liệu an toàn đường bộ DfT](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data) · [Creative Commons CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

Nếu bộ tải kèm các bảng tra mã `contextCSVs`, đặt các CSV đó trong `data/contextCSVs/`. Dùng đúng bảng mã theo phiên bản nguồn. Các CSV tra mã và bốn bảng xử lý được giữ cục bộ.

### Mở notebook và kiểm tra đầu vào

Từ thư mục gốc, chạy `jupyter notebook` trên máy cá nhân hoặc `jupyter notebook --no-browser` trên Cloud. Chọn kernel **Python 3 (ipykernel)** thuộc môi trường vừa kích hoạt. Nếu cần kiểm tra, in `sys.executable` từ một cell.

Trong notebook 01, có thể dùng đoạn dưới đây để kiểm tra tên tệp và xem cấu trúc trước khi đọc toàn bộ ba bảng lớn.

```python
from pathlib import Path

import pandas as pd

# Notebook có thể chạy từ thư mục gốc hoặc từ notebooks/.
root = Path.cwd()
if root.name == "notebooks":
    root = root.parent

expected_keys = {
    "Accidents0515.csv": ["Accident_Index"],
    "Vehicles0515.csv": ["Accident_Index", "Vehicle_Reference"],
    "Casualties0515.csv": ["Accident_Index", "Casualty_Reference", "Vehicle_Reference"],
}

for filename, keys in expected_keys.items():
    csv_path = root / "data" / "raw" / filename
    if not csv_path.is_file():
        raise FileNotFoundError(f"Thiếu tệp {csv_path}")

    columns = pd.read_csv(csv_path, nrows=0, index_col=False).columns
    missing = set(keys) - set(columns)
    if missing:
        raise ValueError(f"{filename} thiếu cột {sorted(missing)}")

    # Chỉ đọc khóa theo tên vì bản lịch sử có dòng thêm trường cuối.
    sample = pd.read_csv(
        csv_path, nrows=5, usecols=keys, index_col=False,
        dtype={"Accident_Index": "string"},
    )
    print(filename, len(columns), "cột có tên")
    print(sample[keys].head(2))
```

Đoạn kiểm tra đọc mẫu nhỏ. Sau khi xác nhận cột, dùng `usecols` để đọc các trường cần thiết và `chunksize` khi thống kê một tệp quá lớn so với RAM. Kiểm tra thêm số dòng đầy đủ, khoảng năm, mã bất thường và khóa chưa ghép được trong notebook 01. Bản `Casualties0515.csv` đính kèm đã kiểm tra có **2.402.909 dòng dữ liệu và 15 cột**. Nhóm cần xác nhận lại kích thước và schema của cả ba tệp trên máy đang chạy.

## 2. Thành viên và phân công

Điền họ tên và MSSV trước khi nộp. Mỗi người phụ trách hai câu và review phần của người khác.

| Vai trò | Họ tên và MSSV | Câu phụ trách | Trách nhiệm chung |
| --- | --- | --- | --- |
| A | Nhóm điền | Q1, Q6 | Xu hướng KSI, mô hình điều phối cấp cứu và đánh giá theo thời gian. |
| B | Nhóm điền | Q2, Q3 | Kiểm tra nguồn, chuẩn hóa và ghép dữ liệu, phân tích nhóm dễ tổn thương và chiếu sáng. |
| C | Nhóm điền | Q4, Q5 | Phân tích mặt đường, trượt/lật và IMD. Kiểm tra tích hợp và điều phối slide. |

## 3. Câu hỏi và bước chuẩn bị dữ liệu

| Mã | Chủ đề | Dữ liệu đầu vào từ notebook 01 |
| --- | --- | --- |
| Q1 | Xu hướng KSI và loại đường, theo tốc độ và đô thị/nông thôn | `accident_counts.csv` |
| Q2 | Nhóm dễ tổn thương, điểm va chạm và thao tác lái | `casualty_vehicle.csv`, `accidents_clean.csv` |
| Q3 | Chiếu sáng, giờ khuya và chênh lệch KSI | `accidents_clean.csv` |
| Q4 | Mặt đường, trượt/lật và phân vùng theo vĩ độ | `vehicle_accident.csv`, `accidents_clean.csv` |
| Q5 | Thương vong và IMD giai đoạn 2011–2015 | `accident_counts.csv`, `vehicle_accident.csv`, `casualty_vehicle.csv` |
| Q6 | Dự đoán KSI khi nhận tin báo 999 | `accidents_clean.csv` |

Chạy lại notebook 01 sau khi cập nhật repo để tạo schema mới. Nhãn `is_ksi` lấy từ mức độ vụ 1/2 (KSI) và 3 (Slight); mã khác để thiếu. Với Q6, dùng 2005–2013 cho train, kiểm định tiến thời gian trong train và giữ 2014–2015 cho test. Chỉ dùng đặc trưng có căn cứ sẵn có lúc nhận cuộc gọi.

Q5 kiểm tra riêng IMD tại nơi xảy ra vụ, nơi cư trú của tài xế và nơi cư trú của người bị nạn. Bản Casualties đã kiểm tra thiếu cột IMD có tên trong tiêu đề. Một số dòng có thêm trường cuối nhưng trường đó chưa được xác minh. Notebook 01 giữ trống IMD và notebook Q5 báo độ phủ. Cần nguồn bổ sung đã xác minh nếu thiếu chỉ số cần phân tích.

Các tỷ lệ mô tả các vụ được ghi nhận và có mẫu số hợp lệ. Xem tiêu chí, giả thuyết và lộ trình đầy đủ trong [question.md](question.md).

## 4. Luồng notebook và quy ước trình bày

1. [Notebook 01](notebooks/01_collection_exploration.ipynb) ghi nguồn, quyền sử dụng, công trình liên quan, động cơ chọn dữ liệu và năm nhóm khám phá theo mục 3.2 của đề bài gồm tổng quan, cột định lượng, cột phân loại, dữ liệu thiếu và mối quan hệ. Kết phần khám phá bằng 3–5 quan sát, vấn đề chất lượng, kế hoạch tiền xử lý và mẫu hình giúp đặt câu hỏi. Sau đó làm sạch và tạo các bảng đầu ra dùng chung.
2. [Notebook 02](notebooks/02_analysis.ipynb) là mục lục và nơi tổng kết. Q1–Q5 có notebook phân tích riêng. [Notebook 03](notebooks/03_ml_question.ipynb) trình bày Q6. Một số tên tệp giữ số cũ theo `question.md`, nên dùng mã câu trong tiêu đề hoặc mục lục. [Phân công và bảng bàn giao](PHAN_CONG.md)
3. Để ghép bảng, kiểm tra khóa trùng và khóa thiếu trước. Ghi số dòng trước và sau, quy tắc xử lý khóa không khớp và quan hệ kỳ vọng, ví dụ `validate="many_to_one"` khi casualty nối với một phương tiện. Tổng hợp từng bảng con về cấp vụ trước khi kết hợp các chỉ số cấp vụ.
4. Mỗi câu viết theo thứ tự câu hỏi và người dùng, mẫu, tiền xử lý, phương pháp, kết quả, giới hạn. Báo số dòng trước và sau từng bước lọc hoặc ghép. Mỗi câu có ít nhất hai hình khác mục đích, có tên trục, đơn vị, chú giải và phạm vi dữ liệu. Kết luận dùng số liệu và diễn giải thực tế.
5. Đặt import, đường dẫn và seed ở đầu. Đặt tên file, hàm và biến bằng `snake_case` cho phần nhóm tự tạo. Lưu dữ liệu sinh lại trong `data/processed/`. Khởi động lại kernel, chạy notebook 01 để tạo dữ liệu, rồi chạy từng notebook câu hỏi trong mục lục trước khi review. Giữ phần logic thực sự dùng chung trong `src/`.

## 5. Làm việc bằng Git và chuẩn bị nộp

Mỗi chủ câu tạo một nhánh từ `vnhatminh` sau khi cập nhật. Xem `git status` trước khi chuyển nhánh và stage theo đường dẫn cụ thể.

```bash
git switch vnhatminh
git pull --ff-only origin vnhatminh
git switch -c feat/b-q02-q03
```

Sau khi hoàn thành, commit notebook và mã liên quan, push nhánh công việc rồi mở pull request vào `vnhatminh`. Ghi đầu vào, cách chạy, số dòng thay đổi và ảnh hoặc bảng chính. Người review chạy lại phần liên quan. Cả nhóm duyệt bản tích hợp trước khi đưa lên `main`.

| Mốc nội bộ | Việc cần hoàn tất |
| --- | --- |
| Trước hạn khoảng 14 ngày | Điền thành viên, xác minh dữ liệu và điều khoản, xin duyệt, lập danh sách công trình công khai liên quan. |
| Trước hạn khoảng 10 ngày | Hoàn thành khám phá, chốt khóa và cách lọc, xác nhận hai câu của mỗi người. |
| Trước hạn khoảng 7 ngày | Câu hỏi có bảng/biểu đồ sơ bộ, ML có baseline và cách chia tập đã được review. |
| Trước hạn khoảng 3 ngày | Chạy toàn bộ notebook từ môi trường sạch, chốt kết luận, giới hạn và 3–5 phát hiện chính. |
| Trước khi nộp | Chuẩn bị [slides.pdf](slides.pdf), cập nhật [nhật ký LLM](LLM_USAGE.md), hoàn tất phản ánh cá nhân và tập trình bày. |

Bài bảo vệ gồm **15 phút trình bày và 10 phút hỏi đáp**. Mỗi thành viên trình bày câu mình phụ trách và chuẩn bị giải thích các phần còn lại. Nhóm tự thực hiện phân tích, trả lời câu hỏi và viết phản ánh theo quy định môn học. Ghi nguồn tài liệu, công trình và đoạn mã tham khảo, cũng như những lần dùng LLM đáng kể. Các mục phân công, kết quả và tài liệu nguồn còn thiếu cần được hoàn thiện trước khi nộp. [Đề bài chính thức](CSC17104_2026_Final_Project.pdf)
