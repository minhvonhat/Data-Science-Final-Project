# Phân công đồ án cho nhóm 3 người

**Phương án:** A và B là hai người phát triển chính. A phụ trách phân tích xu hướng và học máy. B phụ trách dữ liệu chung, phép ghép và phân tích chuyên đề. C phụ trách kiểm tra độ phủ dữ liệu, phân tích bổ sung, kiểm thử tích hợp và chuẩn bị bản nộp.

Mỗi người vẫn sở hữu hai câu hỏi, tự thực hiện phần phân tích của mình và trình bày khi bảo vệ. A, B, C là vai trò để nhóm điền tên và MSSV. Mã câu hỏi giữ theo tài liệu dự án. [Hướng dẫn chung](HUONG_DAN.md) · [Đề bài](CSC17104_2026_Final_Project.pdf)

## 1. Ai làm gì và được sửa tệp nào

Các đường dẫn mới dưới đây là vị trí sẽ tạo khi triển khai. Mỗi notebook chỉ có một chủ sở hữu.

| Người | Câu hỏi và trách nhiệm | Tệp hoặc thư mục được sửa | Đầu ra để bàn giao |
| --- | --- | --- | --- |
| **A · Code chính** · Tên/MSSV: … | **Q01** phân tích tỷ lệ tai nạn nghiêm trọng theo thời gian và cơ cấu loại đường. **Q02** so sánh baseline và hai mô hình dự đoán mức độ nghiêm trọng. | `notebooks/02_q01_xu_huong.ipynb`, [`notebooks/03_ml_question.ipynb`](notebooks/03_ml_question.ipynb), `src/modeling/` | Q01 có bảng tỷ lệ và biểu đồ thời gian. Q02 có thiết kế chia tập, bảng CV và đánh giá test, biểu đồ sai số và diễn giải. |
| **B · Code chính** · Tên/MSSV: … | Làm notebook thu thập, khám phá và tạo bảng xử lý dùng chung. **Q03** so sánh thương tích nghiêm trọng theo nhóm tuổi và phương tiện. **Q04** phân tích điều kiện ánh sáng và độ nhạy với mã thiếu. | [`notebooks/01_collection_exploration.ipynb`](notebooks/01_collection_exploration.ipynb), `notebooks/02_q03_thuong_tich.ipynb`, `notebooks/02_q04_anh_sang.ipynb`, `src/data_prep/` | Dữ liệu xử lý có schema và thống kê kiểm tra, Q03 có khoảng tin cậy, Q04 có so sánh hai quy tắc xử lý mã thiếu. |
| **C · Hỗ trợ** · Tên/MSSV: … | **Q05** kiểm tra độ phủ của phép ghép. **Q06** phân tích số người bị nạn theo số phương tiện ở cấp vụ. Chạy kiểm thử tích hợp, tổng hợp slide và sổ bàn giao. | `notebooks/02_q05_do_phu.ipynb`, `notebooks/02_q06_so_nguoi_bi_nan.ipynb`, [`notebooks/02_analysis.ipynb`](notebooks/02_analysis.ipynb) làm mục lục, [`slides.pdf`](slides.pdf) | Bảng số dòng ghép được và chưa ghép được, kết quả Q06, biên bản chạy lại và PDF cuối. |

- **A** làm tính năng, tiền xử lý riêng cho Q02 và mô hình bên trong pipeline. A dùng bảng dữ liệu chung của B cho cả hai câu và báo vấn đề schema trong pull request của B.
- **B** sở hữu mọi thay đổi tới cách đọc CSV, chuẩn hóa mã, kiểm tra khóa, nối bảng và xuất dữ liệu dùng chung. B giữ các bộ lọc riêng của Q03 và Q04 trong notebook của mình.
- **C** dùng bảng đã xử lý để trả lời hai câu. Q05 báo tỷ lệ ghép trên toàn bộ người bị nạn, rồi tính lại trên nhóm có đủ khóa để cho thấy ảnh hưởng của mẫu số. Q06 dùng bảng cấp vụ để so sánh phân phối và chênh lệch theo loại đường. Tính khoảng tin cậy bằng cách lấy mẫu lại theo vụ trong các nhóm đủ mẫu. Mỗi câu vẫn có bằng chứng và ít nhất hai biểu đồ có nhãn.
- **Tệp chung:** C tổng hợp `README.md`, `HUONG_DAN.md`, `LLM_USAGE.md` và slide khi cần, từ nội dung mỗi người gửi. B quản lý `environment.yml` nếu cần thêm thư viện sau khi cả nhóm thống nhất. A và B gửi nội dung hoặc mở góp ý cho chủ tệp. C cập nhật notebook mục lục sau khi các notebook câu hỏi đã được merge.

## 2. Chốt đầu vào và đầu ra trước khi bắt đầu code

B tạo các bảng dưới đây từ ba CSV gốc. A và C đọc chúng để triển khai phần riêng. Tên cột tập trung ở đây để cả nhóm thống nhất ngay ngày đầu. Nếu dữ liệu thực yêu cầu thay đổi, B đề xuất qua pull request trước khi đổi.

| Bảng xử lý trong `data/processed/` | Đơn vị và khóa | Cột tối thiểu | Người dùng |
| --- | --- | --- | --- |
| `accidents_clean.csv` | Một dòng mỗi vụ, `accident_id` duy nhất | `accident_id`, `accident_date`, `accident_year`, `road_type`, `light_conditions`, `is_severe` | A cho Q01 và Q02, B cho Q04. |
| `casualty_vehicle.csv` | Một dòng mỗi người bị nạn, khóa `accident_id` + `casualty_ref` | `accident_id`, `casualty_ref`, `vehicle_ref`, `accident_year`, `casualty_type`, `age_band`, `vehicle_type`, `casualty_severity`, `vehicle_match_status` | B cho Q03, C cho Q05. Giữ dòng chưa ghép được để Q05 có mẫu số ban đầu. |
| `accident_counts.csv` | Một dòng mỗi vụ, `accident_id` duy nhất | `accident_id`, `road_type`, `n_vehicles`, `n_casualties` | C cho Q06. B tổng hợp từng bảng con về cấp vụ trước khi ghép. |

Quy ước khi bàn giao:

- Đọc `accident_id` dưới dạng chuỗi để giữ nguyên khóa. Ngày ghi theo `YYYY-MM-DD`. Mã loại và nhãn nghiêm trọng theo từ điển dữ liệu mà B ghi trong notebook 01. Giá trị thiếu lưu thành ô trống. Với số đếm, chỉ ghi `0` khi xác định thật sự bằng không.
- B xác nhận khóa và quan hệ ghép trước khi xuất bảng. Ghi số dòng trước/sau, số khóa thiếu hoặc trùng, số dòng ghép được và chưa ghép được. `vehicle_match_status` phân biệt `matched`, `missing_key` và `unmatched`. Công bố rõ cách xử lý bản ghi trùng nếu có.
- A dùng ngày để chia tập. `is_severe` là nhãn. Chỉ đưa vào mô hình các đặc trưng có thể biết lúc ghi nhận ban đầu. Các số đếm hậu quả từ `accident_counts.csv` dùng cho Q06.
- Các bảng xử lý được tạo lại bằng notebook 01. Mỗi câu ghi bảng/ảnh riêng dưới `data/processed/q01/`, `q02/` … nếu cần xuất ra tệp. Trong PR, gửi schema, số dòng và cách tạo lại dữ liệu. CSV thực nằm trong thư mục dữ liệu được Git bỏ qua.
- Nếu chưa có dữ liệu xử lý, A và C có thể dựng một mẫu giả nhỏ từ schema để thử đường dẫn và logic. Kết quả báo cáo chỉ dùng dữ liệu thật sau khi chạy lại.

### Nhịp bàn giao để A và B làm song song

| Mốc | A làm gì | B làm gì | C làm gì |
| --- | --- | --- | --- |
| **Buổi 1 · Chốt bảng và câu hỏi** | Chốt cột cần cho Q01, Q02, nhãn dự kiến và cách chia thời gian. | Đối chiếu tên cột gốc, khóa và giá trị thiếu. Xác nhận ba bảng đầu ra cùng cả nhóm. | Chốt checklist, mẫu biểu đồ, mẫu số của Q05 và cỡ nhóm tối thiểu để báo Q06. |
| **Trong khi B chuẩn bị dữ liệu** | Viết notebook Q01 và pipeline Q02 trên mẫu nhỏ có schema đã chốt. Để sẵn bước kiểm tra cột khi mở bảng thật. | Viết notebook 01 và kiểm tra bảng xuất. Mở PR dữ liệu trước để A và C review. | Viết khung Q05/Q06, rà nguồn, điều khoản sử dụng và checklist bàn giao. |
| **Khi PR dữ liệu được merge** | Cập nhật nhánh, tạo lại dữ liệu thật, hoàn tất Q01 và huấn luyện Q02. | Làm Q03/Q04 trên bảng chung. | Chạy Q05/Q06, tái lập notebook 01 và ghi các lỗi cùng bước tái hiện. |
| **Trước ngày nộp 2–3 ngày** | Review phép ghép và giới hạn diễn giải của B. Chốt biểu đồ mô hình và kết quả của A. | Review chia tập, rò rỉ đặc trưng và thước đo của A. Chốt kết quả của B. | Chạy lại toàn bộ từ kernel mới, hoàn tất biểu đồ Q05/Q06, mục lục, slide và checklist. |

## 3. Nhánh Git và thứ tự tích hợp

`vnhatminh` là nhánh tích hợp. Mỗi người tạo nhánh riêng từ cùng phiên bản đã cập nhật. Ví dụ khi bắt đầu phần A:

```bash
git switch vnhatminh
git pull --ff-only origin vnhatminh
git switch -c feat/a-xu-huong-ml
```

| Người | Nhánh | PR kéo vào `vnhatminh` |
| --- | --- | --- |
| B | `feat/b-du-lieu-chung` | Notebook 01 và code tạo bảng. A review schema và cách tái lập trước. |
| A | `feat/a-xu-huong-ml` | Q01 và Q02. Có thể mở PR nháp sớm, rồi cập nhật nhánh sau khi PR dữ liệu được merge. |
| B | `feat/b-q03-q04` | Tạo từ `vnhatminh` sau khi PR dữ liệu đã vào. Chỉ chứa Q03/Q04 và code riêng liên quan. |
| C | `feat/c-kiem-tra-tong-hop` | Q05/Q06 và phần tổng hợp. Hoàn tất mục lục và slide sau khi nhận kết quả của A, B. |

Trong nhánh riêng, lấy thay đổi đã tích hợp bằng `git fetch origin` rồi `git merge origin/vnhatminh` khi thư mục làm việc sạch. Trước khi commit, xem `git status --short` và stage từng đường dẫn được giao. Trong PR, ghi notebook đã chạy, phiên bản dữ liệu, cỡ mẫu chính và mục cần review. Nếu cần sửa tệp do người khác sở hữu, báo chủ tệp để người đó sửa. Nếu đổi schema, ghi cả tên cột cũ và mới, lý do đổi và các notebook bị ảnh hưởng trong cùng PR.

**Thứ tự merge:** dữ liệu chung → Q01/Q02 và Q03/Q04 theo thứ tự PR nào sẵn sàng trước → Q05/Q06 và tổng hợp. Sau vòng chạy cuối, nhóm duyệt phiên bản nộp để đưa lên `main`.

## 4. Checklist để chốt công việc

- [ ] **B bàn giao dữ liệu:** notebook 01 chạy từ ba CSV tải theo hướng dẫn, tái tạo ba bảng, có thống kê dòng trước/sau và kiểm tra khóa.
- [ ] **A bàn giao nghiên cứu:** Q01 có cơ cấu so sánh và bằng chứng theo thời gian. Q02 có baseline, hai mô hình, pipeline, CV chỉ trên train, test theo thời gian, phân tích sai số và diễn giải.
- [ ] **B bàn giao nghiên cứu:** Q03 có phép ghép và khoảng tin cậy. Q04 có so sánh theo loại đường, kiểm tra độ nhạy và giới hạn.
- [ ] **C bàn giao nghiên cứu và tích hợp:** Q05 có mẫu số và thống kê trạng thái ghép. Q06 tính ở cấp vụ, có cỡ mẫu và biểu đồ. Mục lục chỉ đúng thứ tự chạy và slide khớp với notebook.
- [ ] **Cả nhóm review:** mỗi câu có chủ sở hữu, mô tả mẫu, ít nhất hai biểu đồ và câu trả lời bằng số liệu. Mỗi người kiểm tra một phần của người khác, tự viết phản ánh và chuẩn bị trình bày hai câu của mình.
