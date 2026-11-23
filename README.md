# Data-Science-Final-Project

## Thành viên nhóm

| Họ và tên | MSSV | Câu hỏi phụ trách | Công việc |
| --- | --- | --- | --- |
| … | … | … | … |

## Bộ dữ liệu

- Mô tả và đơn vị quan sát
- Nguồn, đơn vị thu thập và đường dẫn tải
- Giấy phép và yêu cầu ghi công
- Notebook hoặc phân tích công khai liên quan và điểm khác biệt của đề tài

## Câu hỏi nghiên cứu

Liệt kê hai câu hỏi cho mỗi thành viên, trong đó có ít nhất một câu hỏi dùng mô hình học máy.

| Mã | Câu hỏi | Người phụ trách | Phương pháp |
| --- | --- | --- | --- |
| … | … | … | … |

## Kết quả chính

Cập nhật sau khi hoàn thành phân tích.

## Cách chạy dự án

1. Tạo và kích hoạt môi trường Conda từ thư mục gốc của dự án.

   ```bash
   conda env create -f environment.yml
   conda activate data-science-final-project
   ```

2. Tải dữ liệu từ nguồn ghi ở mục **Bộ dữ liệu** và đặt các tệp gốc vào `data/raw/`. Lưu dữ liệu qua xử lý vào `data/processed/`.
3. Chạy `jupyter lab` từ thư mục gốc và mở các notebook theo thứ tự sau.
   1. [Thu thập và khám phá dữ liệu](notebooks/01_collection_exploration.ipynb)
   2. [Phân tích dữ liệu](notebooks/02_analysis.ipynb)
   3. [Câu hỏi học máy](notebooks/03_ml_question.ipynb)
