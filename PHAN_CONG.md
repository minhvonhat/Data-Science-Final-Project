# Phân công đồ án cho nhóm 3 người

A phụ trách xu hướng và học máy, B phụ trách dữ liệu chung và hai câu phân tích chuyên đề, C phụ trách hai câu phân tích bổ sung và tích hợp. Mỗi người vẫn sở hữu hai câu và tự thực hiện phần phân tích của mình. Mã câu lấy từ [question.md](question.md).

## 1. Ai làm gì

| Người | Câu và trách nhiệm | Tệp sở hữu |
| --- | --- | --- |
| **A · Code chính** · Tên/MSSV: … | **Q1** xu hướng KSI và loại đường. **Q6** mô hình dự đoán KSI khi nhận tin báo 999. | [Q1](notebooks/02_q01_xu_huong.ipynb), [Q6](notebooks/03_ml_question.ipynb), `src/modeling/` |
| **B · Code chính** · Tên/MSSV: … | Chuẩn bị dữ liệu chung. **Q2** nhóm dễ tổn thương, hướng va chạm và thao tác lái. **Q3** chiếu sáng và mức độ nghiêm trọng. | [Notebook 01](notebooks/01_collection_exploration.ipynb), [Q2](notebooks/02_q03_thuong_tich.ipynb), [Q3](notebooks/02_q04_anh_sang.ipynb), `src/data_prep/` |
| **C · Hỗ trợ** · Tên/MSSV: … | **Q4** mặt đường, trượt/lật và khu vực. **Q5** thương vong và IMD. Kiểm tra tích hợp, tổng hợp bản nộp và slide. | [Q4](notebooks/02_q05_do_phu.ipynb), [Q5](notebooks/02_q06_so_nguoi_bi_nan.ipynb), [mục lục](notebooks/02_analysis.ipynb), [slide](slides.pdf) |

Các tên tệp theo `question.md`. Dùng mã câu bên trong notebook để tránh nhầm với số trong tên cũ. C tổng hợp README, hướng dẫn, nhật ký và slide từ nội dung các thành viên gửi. B quản lý cấu hình môi trường và schema chung. A giữ tiền xử lý dành riêng cho mô hình trong pipeline của Q6.

## 2. Bàn giao dữ liệu

Chạy notebook 01 để tạo bốn CSV cục bộ trong `data/processed/`. Mã chuẩn hóa và ghép bảng nằm ở [road_safety.py](src/data_prep/road_safety.py). Một số cột chủ chốt được liệt kê dưới đây. Notebook mỗi câu kiểm tra trực tiếp các cột đầu vào riêng.

| Bảng | Đơn vị quan sát | Trường dùng để bàn giao |
| --- | --- | --- |
| `accidents_clean.csv` | Một dòng mỗi vụ | Khóa, ngày/năm/tháng/thứ/giờ, loại đường, vùng, tốc độ, tọa độ, ánh sáng, thời tiết, mặt đường, nút giao, mức độ gốc và `is_ksi`. |
| `casualty_vehicle.csv` | Một dòng mỗi người bị nạn | Nhóm tuổi, loại người bị nạn, mức độ thương tích, mã xe, loại xe, điểm va chạm, thao tác lái, năm và `vehicle_match_status`. |
| `vehicle_accident.csv` | Một dòng mỗi phương tiện | Loại xe, trượt/lật, IMD tài xế nếu có, điều kiện vụ, vĩ độ, tốc độ, `is_ksi` và `accident_match`. |
| `accident_counts.csv` | Một dòng mỗi vụ | Các biến phân tầng của Q1/Q5, IMD nơi xảy ra vụ nếu có, số xe, người bị nạn, người tử vong và số người có mã thương tích hợp lệ. |

- Mã vụ là chuỗi. Bảng người bị nạn ghép với xe theo `accident_id + vehicle_ref`; bảng xe ghép với vụ theo `accident_id`. Kiểm tra khóa đầy đủ của người bị nạn bằng `accident_id + vehicle_ref + casualty_ref`. Giữ các dòng bên trái và báo khóa thiếu, trùng, chưa khớp. Đếm xe và người bị nạn riêng trước khi bàn giao ở cấp vụ.
- Dùng `is_ksi` cho nhãn cấp vụ. Tử vong ở cấp người có tử số riêng. Giữ riêng IMD nơi xảy ra vụ, tài xế và người bị nạn. Khi thiếu trường IMD, ghi độ phủ và nguồn cần xác minh.
- B xác minh cấu trúc và phạm vi. A và C có thể viết các bước riêng với mẫu schema nhỏ trong lúc chờ dữ liệu thật. Chạy lại notebook của mình với dữ liệu thật trước khi báo kết quả.

### Nhịp bàn giao để làm song song

| Mốc | A | B | C |
| --- | --- | --- | --- |
| Chốt dữ liệu | Xác nhận cột và nhãn Q1/Q6, đặc trưng có thể biết khi gọi 999. | Kiểm tra ba CSV, khóa ghép, trường dùng chung và phạm vi IMD. | Xác nhận đầu vào Q4/Q5, lập checklist chạy lại và báo cột thiếu. |
| Trong khi B xác minh dữ liệu | Viết khung Q1/Q6 từ schema đã thống nhất, thử logic trên mẫu nhỏ. | Chạy notebook 01 trên dữ liệu thật, bàn giao bốn bảng và ghi số dòng trước/sau. | Lên cách kiểm tra mặt đường và độ phủ IMD, review phép ghép. |
| Sau khi dữ liệu đã được review | Chạy Q1/Q6 và chốt phương án chia thời gian, chỉ số đánh giá. | Hoàn thành Q2/Q3, rà giá trị thiếu và chênh lệch trong cùng tầng. | Hoàn thành Q4/Q5 theo dữ liệu có sẵn, tổng hợp kết quả và tình trạng các hạn chế. |
| Trước hạn 2–3 ngày | Review kết quả và giới hạn của B. | Review việc chia tập và chống rò rỉ của A. | Chạy lại theo mục lục, đối chiếu số liệu trên slide và tổng hợp phản hồi. |

## 3. Nhánh và trình tự tích hợp

| Người | Nhánh công việc | Phần đưa vào `vnhatminh` |
| --- | --- | --- |
| B | `feat/b-du-lieu-chung` | Rà schema, nguồn, các bảng và quy tắc làm sạch trong notebook 01. |
| A | `feat/a-xu-huong-ml` | Q1 và Q6. A review schema và giữ riêng logic mô hình. |
| B | `feat/b-q02-q03` | Q2 và Q3. A review phép ghép và cách so sánh. |
| C | `feat/c-kiem-tra-tong-hop` | Q4 và Q5, kết quả chạy lại toàn bộ và slide. |

Tạo nhánh từ `vnhatminh` mới nhất. Giai đoạn đầu ưu tiên kiểm tra dữ liệu chung. Sau đó A, B và C triển khai notebook riêng song song. Mở PR vào `vnhatminh`, ghi bảng đầu vào, cỡ mẫu và cách chạy. Báo chủ tệp trước khi sửa ngoài phạm vi được giao. Ghép bản hoàn chỉnh vào `main` sau khi nhóm duyệt.

## 4. Checklist bàn giao

- [ ] **B · Dữ liệu** Cả bốn bảng tái tạo được, có báo cáo khóa, mã thiếu và độ phủ IMD.
- [ ] **A · Q1 và Q6** Q1 có xu hướng và so sánh trong cùng tầng. Q6 có baseline, hai mô hình, pipeline, chia thời gian, thước đo và phân tích lỗi.
- [ ] **B · Q2 và Q3** Q2 có phân nhóm tuổi/tốc độ, độ phủ phép ghép và khoảng tin cậy. Q3 có so sánh trong tầng có đủ dữ liệu và kiểm tra độ nhạy.
- [ ] **C · Q4 và Q5** Q4 ghi mẫu số cấp xe/cấp vụ và kiểm tra theo mùa. Q5 báo IMD theo nguồn và theo năm, phân tích khi đủ dữ liệu.
- [ ] **Cả nhóm** Mỗi câu có tối thiểu hai biểu đồ phù hợp, số liệu và giới hạn. Tái chạy các notebook, ghép kết quả với slide, tự viết phản ánh cá nhân và ghi nhật ký sử dụng LLM.
