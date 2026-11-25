# Hướng dẫn thực hiện đồ án CSC17104

Dùng tài liệu này để thiết lập máy, nhận câu hỏi phụ trách, chạy notebook và chuẩn bị bản nộp. Các câu hỏi dưới đây là đề xuất để nhóm xác nhận sau khi kiểm tra dữ liệu và xin duyệt từ giảng viên. [Đề bài chính thức](CSC17104_2026_Final_Project.pdf)

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
| `data/raw/Casualties0515.csv` | Một người bị nạn trong một vụ | `Accident_Index` và `Casualty_Reference`. `Vehicle_Reference` dùng khi cần nối với bảng phương tiện. |

Giữ CSV và ZIP lớn trên máy. Quy tắc `.gitignore` trong repo đã bỏ qua dữ liệu ở `data/raw/` và đầu ra sinh lại ở `data/processed/`. Kiểm tra sau khi tải bằng `git status --short --ignored -- data/raw/`. Ký hiệu `!!` cho biết dữ liệu đang được bỏ qua.

Người phụ trách nguồn ghi phiên bản/ngày tải, tên nguồn phát hành, giấy phép và ghi công hiển thị trên phiên bản Kaggle đã dùng. Đối chiếu ngữ nghĩa các cột, mã phân loại và phạm vi bao phủ với tài liệu STATS19 của Department for Transport. Giấy phép trong repo áp dụng cho phần do nhóm có quyền cấp phép. Dữ liệu gốc tuân theo điều khoản của nguồn phát hành. [Nguồn Kaggle](https://www.kaggle.com/datasets/silicon99/dft-accident-data) · [Tài liệu và dữ liệu an toàn đường bộ DfT](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data) · [Creative Commons CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

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

    # Xem mẫu nhỏ để kiểm tra schema. Giữ mã vụ tai nạn dưới dạng chuỗi.
    sample = pd.read_csv(csv_path, nrows=5, dtype={"Accident_Index": "string"})
    missing = set(keys) - set(sample.columns)
    if missing:
        raise ValueError(f"{filename} thiếu cột {sorted(missing)}")
    print(filename, sample.shape[1], "cột")
    print(sample[keys].head(2))
```

Đoạn kiểm tra đọc mẫu nhỏ. Sau khi xác nhận cột, dùng `usecols` để đọc các trường cần thiết và `chunksize` khi thống kê một tệp quá lớn so với RAM. Kiểm tra thêm số dòng đầy đủ, khoảng năm, mã bất thường và khóa chưa ghép được trong notebook 01. Bản `Casualties0515.csv` đính kèm đã kiểm tra có **2.402.909 dòng dữ liệu và 15 cột**. Nhóm cần xác nhận lại kích thước và schema của cả ba tệp trên máy đang chạy.

## 2. Thành viên và phân công

Điền họ tên và MSSV trước khi nộp. Nhóm hai người làm Q01–Q04. Nhóm ba người thêm Q05–Q06. Mỗi người phụ trách hai câu và review phần của người khác.

| Vai trò | Họ tên và MSSV | Câu phụ trách | Trách nhiệm chung |
| --- | --- | --- | --- |
| A | Nhóm điền | Q01, Q02 | Điều phối tiến độ, chốt cách chia tập và bảng đánh giá ML, kiểm tra khả năng tái lập. |
| B | Nhóm điền | Q03, Q04 | Xác minh nguồn và quyền sử dụng, xây dựng từ điển dữ liệu, kiểm tra khóa và phép ghép. |
| C, nếu có | Nhóm điền | Q05, Q06 | Kiểm tra độ phủ dữ liệu, chuẩn hóa biểu đồ và điều phối slide. |

Nếu có hai người, B điều phối slide và A rà soát bản nộp cuối. Chủ câu thực hiện notebook, chuẩn bị hình minh họa, ghi cỡ mẫu và kết luận, mở pull request. Cả nhóm thống nhất cách ghép và quy tắc làm sạch trước khi chia việc.

## 3. Câu hỏi và thiết kế đề xuất

Mỗi câu phân tích dùng tối thiểu hai tiêu chí độ sâu trong đề bài. Cả nhóm cần phủ tối thiểu bốn trong D1–D6. Các câu dưới đây dùng D1–D6 theo nghĩa ghi trong đề bài. Báo rõ đơn vị quan sát, mẫu số và giới hạn trước khi so sánh. Số vụ trong dữ liệu mô tả các vụ được ghi nhận. Muốn ước tính rủi ro trên mỗi chuyến đi cần thêm dữ liệu về mức độ tham gia giao thông.

| Mã | Câu hỏi và người dùng | Phương pháp dự kiến |
| --- | --- | --- |
| Q01 | Tỷ lệ vụ nghiêm trọng trong số vụ được ghi nhận thay đổi thế nào theo tháng và năm, sau khi giữ cố định cơ cấu loại đường? Kết quả giúp người lập kế hoạch an toàn giao thông thấy biến động theo thời gian. | **D2, D3, D4.** Chuẩn hóa ngày, tính tỷ lệ theo tháng và loại đường. So chuỗi tỷ lệ chung với chuỗi có trọng số loại đường cố định. Vẽ chuỗi thời gian và mức thay đổi theo loại đường. |
| Q02 | Với các trường có thể biết khi ghi nhận ban đầu, mô hình nhận diện vụ nghiêm trọng trên giai đoạn mới tốt hơn mốc đơn giản bao nhiêu? Người dùng là nhóm phân tích an toàn giao thông. | **ML.** Phân loại ở cấp vụ bằng DummyClassifier, LogisticRegression và RandomForestClassifier. Chia theo thời gian và trình bày average precision, sai số theo nhóm cùng các giới hạn. |
| Q03 | Tỷ lệ người bị nạn có thương tích nghiêm trọng khác nhau thế nào theo nhóm phương tiện trong cùng nhóm tuổi? Người đọc dùng kết quả để hiểu khác biệt giữa các nhóm trong hồ sơ đã ghi nhận. | **D1, D4, D5.** Ghép casualty với phương tiện theo khóa ghép sau khi kiểm tra quan hệ nhiều-một. Tính tỷ lệ và khoảng tin cậy bootstrap theo cụm vụ. Vẽ tỷ lệ theo nhóm và chênh lệch kèm khoảng tin cậy. |
| Q04 | Chênh lệch tỷ lệ vụ nghiêm trọng giữa các nhóm điều kiện ánh sáng có còn khi so trong cùng loại đường, và nhạy đến đâu với mã thiếu hoặc không rõ? | **D3, D4, D6.** Tạo biến phân loại mức độ nghiêm trọng sau khi đối chiếu mã, so theo tầng loại đường và lặp với quy tắc xử lý mã không rõ khác. Vẽ tỷ lệ theo tầng và thay đổi giữa hai kịch bản. |
| Q05 | Độ phủ khi ghép người bị nạn với phương tiện thay đổi ra sao theo năm và loại người tham gia giao thông? Người phân tích dùng kết quả để đánh giá sai lệch khi chọn mẫu ghép. | **D1, D2, D6.** Đếm khóa ghép được và thiếu theo năm và nhóm. So kết quả khi xử lý các trường hợp thiếu khóa theo hai quy tắc có giải thích. |
| Q06 | Trong các vụ ở điều kiện đường tương tự, số người bị nạn trên mỗi vụ thay đổi thế nào theo số phương tiện liên quan? | **D1, D3, D4, D5.** Tổng hợp phương tiện và người bị nạn về cấp vụ trước khi ghép. Báo phân phối, chênh lệch theo tầng và độ bất định. |

Với Q02, chốt nhãn nghiêm trọng dựa trên tài liệu mã hóa và xác định thời điểm từng đặc trưng có sẵn. Giữ `Accident_Index` làm khóa, dùng ngày để chia tập, bỏ nhãn, mức độ thương tích và các biến tổng hợp hậu quả khỏi đặc trưng. Dùng các năm đầu để huấn luyện và các năm cuối để kiểm tra, sau khi đã xác minh phạm vi năm. Dùng cross-validation theo thời gian trên train. Nếu có nhiều dòng trên một vụ, đưa về một dòng mỗi vụ trước khi chia hoặc giữ mọi dòng cùng vụ trong cùng tập.

Đặt bước điền thiếu và mã hóa bên trong `Pipeline`, dùng cùng các tập cho baseline và hai mô hình, chọn metric và ngưỡng bằng validation rồi đánh giá test một lượt. Với lớp nghiêm trọng hiếm, dùng average precision để tóm tắt đường precision–recall, kèm precision và recall ở ngưỡng đã chốt. Vẽ đường precision–recall và biểu đồ sai sót theo nhóm, giải thích mô hình bằng permutation importance trên validation. Ghi rõ điều kiện thực tế để mô hình có thể sử dụng được.

## 4. Luồng notebook và quy ước trình bày

1. [Notebook 01](notebooks/01_collection_exploration.ipynb) ghi nguồn, quyền sử dụng, công trình liên quan, định nghĩa một dòng mỗi bảng, từ điển cột, số lượng/mẫu thiếu, khoảng thời gian và ngoại lệ. Kết phần khám phá bằng 3–5 quan sát, các quyết định tiền xử lý và đường dẫn đầu ra dùng chung.
2. [Notebook 02](notebooks/02_analysis.ipynb) là mục lục và nơi tổng kết. Q01, Q03, Q04, Q05 và Q06 có notebook riêng theo người phụ trách. [Notebook 03](notebooks/03_ml_question.ipynb) trình bày Q02. Mỗi notebook đã có sườn và cell kiểm tra đầu vào để bắt đầu. [Phân công và bảng bàn giao](PHAN_CONG.md)
3. Để ghép bảng, kiểm tra khóa trùng và khóa thiếu trước. Ghi số dòng trước và sau, quy tắc xử lý khóa không khớp và quan hệ kỳ vọng, ví dụ `validate="many_to_one"` khi casualty nối với một phương tiện. Tổng hợp từng bảng con về cấp vụ trước khi kết hợp các chỉ số cấp vụ.
4. Mỗi câu viết theo thứ tự câu hỏi và người dùng, mẫu, tiền xử lý, phương pháp, kết quả, giới hạn. Báo số dòng trước và sau từng bước lọc hoặc ghép. Mỗi câu có ít nhất hai hình khác mục đích, có tên trục, đơn vị, chú giải và phạm vi dữ liệu. Kết luận dùng số liệu và diễn giải thực tế.
5. Đặt import, đường dẫn và seed ở đầu. Đặt tên file, hàm và biến bằng `snake_case` cho phần nhóm tự tạo. Lưu dữ liệu sinh lại trong `data/processed/`. Khởi động lại kernel, chạy notebook 01 để tạo dữ liệu, rồi chạy từng notebook câu hỏi trong mục lục trước khi review. Giữ phần logic thực sự dùng chung trong `src/`.

## 5. Làm việc bằng Git và chuẩn bị nộp

Mỗi chủ câu tạo một nhánh từ `vnhatminh` sau khi cập nhật. Xem `git status` trước khi chuyển nhánh và stage theo đường dẫn cụ thể.

```bash
git switch vnhatminh
git pull --ff-only origin vnhatminh
git switch -c q03-phan-tich-nguoi-bi-nan
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
