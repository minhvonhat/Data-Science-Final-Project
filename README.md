# Phân tích giao dịch bất động sản New York City

Đồ án cuối kỳ môn **CSC17104 – Programming for Data Science**, Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM. Nhóm dùng hồ sơ giao dịch tại New York City từ tháng 9/2016 đến tháng 8/2017 để nghiên cứu biến động giá, so sánh các nhóm nhà ở và đánh giá khả năng dự đoán giá cho bất động sản chưa xuất hiện trong dữ liệu huấn luyện.

README này là kế hoạch làm việc trên nhánh `vnhatminh`. Repo hiện có CSV gốc, cấu hình môi trường, ba notebook khung và một trang bìa slide. Nhóm sẽ chốt phân công và phương pháp sau khi xác nhận bộ dữ liệu với giảng viên, rồi cập nhật kết quả từ notebook đã chạy.

**Đề bài** · [CSC17104_2026_Final_Project.pdf](CSC17104_2026_Final_Project.pdf)

## Yêu cầu và sản phẩm bàn giao

| Hạng mục | Điều kiện hoàn thành |
| --- | --- |
| Nhóm và dữ liệu | Nhóm 2–3 sinh viên. Xin duyệt dữ liệu thực, công khai, có nguồn và điều kiện sử dụng phục vụ học tập. Quy mô tham chiếu tối thiểu khoảng 3.000 dòng và 10 cột. |
| Câu hỏi | Mỗi người đứng tên đúng hai câu, tổng cộng 4 hoặc 6. Cả nhóm có ít nhất một câu ML. Mỗi câu phân tích có ít nhất hai tiêu chí D1–D6 và các câu phân tích phải phủ ít nhất bốn tiêu chí khác nhau. |
| Phân tích | Mỗi câu có động cơ, đối tượng sử dụng, phương pháp, số dòng trước và sau những bước thay đổi dữ liệu, ít nhất hai biểu đồ có nhãn, câu trả lời bằng số liệu và giới hạn diễn giải. |
| Tổng kết | Chọn 3–5 phát hiện chính, nêu phát hiện bất ngờ nhất, giới hạn và hướng phát triển. Mỗi người tự viết phản ánh về khó khăn, cách xử lý, điều đã học và cách đã dùng LLM. |
| Repo | README, `environment.yml`, [`LLM_USAGE.md`](LLM_USAGE.md), các thư mục dữ liệu, notebook, mã dùng chung trong `src/` và [`slides.pdf`](slides.pdf). Người khác có thể dựng môi trường và chạy từ CSV gốc. |
| Bảo vệ | Trình bày 15 phút, hỏi đáp 10 phút. Mỗi người trình bày câu mình phụ trách và hiểu các phần còn lại. Điểm cá nhân có thể khác nhau theo hỏi đáp và lịch sử Git. |

## Thành viên và phân công

Điền tên thật và MSSV trước khi gửi đề xuất. A, B và C là vai trò để nhóm tự gán. Với nhóm hai người, dùng A–B và làm Q01–Q04. Với nhóm ba người, thêm C và Q05–Q06.

| Vai trò | Họ và tên | MSSV | Câu sở hữu | Trách nhiệm chung |
| --- | --- | --- | --- | --- |
| A | Nhóm điền | Nhóm điền | Q01, Q02 | Theo dõi mốc tích hợp, dựng quy trình ML, kiểm tra khả năng tái lập. |
| B | Nhóm điền | Nhóm điền | Q03, Q04 | Đối chiếu nguồn, giấy phép và bản ghi; điều phối từ điển dữ liệu, kiểm tra chất lượng và quy tắc làm sạch. |
| C, nếu nhóm có 3 người | Nhóm điền | Nhóm điền | Q05, Q06 | Kiểm tra độ phủ và độ nhạy, thống nhất biểu đồ, điều phối slide và buổi tập bảo vệ. |

Với hai người, B phụ trách thêm bố cục slide, A ghép bản nộp. Mỗi chủ câu viết code, giải thích phương pháp, lưu bằng chứng, chuẩn bị slide của mình và mở pull request. Hai người review chéo. Ba người review theo vòng A → B → C → A, trong đó mũi tên chỉ người review bài của người kế tiếp. Cả nhóm duyệt quy tắc làm sạch, câu hỏi và mẫu phân tích chung trước khi phân tích riêng.

## Dữ liệu, nguồn và công trình liên quan

- Mỗi dòng là **một bản ghi giao dịch hoặc chuyển nhượng** bất động sản. Một thửa có thể xuất hiện nhiều lần. Dữ liệu mô tả các giao dịch được ghi nhận, nên khả năng suy rộng sang toàn bộ nhà ở NYC hoặc thị trường hiện tại có giới hạn.
- CSV trong repo có **84.548 dòng và 22 cột**, tính cả cột đầu không tên dùng làm chỉ số xuất tệp. Ngày giao dịch từ **01/09/2016 đến 31/08/2017**. Dữ liệu gồm Manhattan (1), Bronx (2), Brooklyn (3), Queens (4) và Staten Island (5). [CSV trong repo](data/raw/nyc-rolling-sales.csv)
- NYC Department of Finance công bố hồ sơ hành chính về giao dịch bất động sản. Nhóm đối chiếu bộ cột, định nghĩa giá chuyển nhượng, quy trình ghi nhận và kỳ báo cáo với trang chính thức. Bản CSV trong repo trùng SHA-256 với bản lưu công khai trong repo của Varsha Budihal. Trang Kaggle là đầu mối để xác nhận gói tải lịch sử, người đăng và ngày công bố chính xác. [NYC Department of Finance](https://www.nyc.gov/site/finance/taxes/property-rolling-sales-data.page) · [Kaggle NYC Rolling Sales](https://www.kaggle.com/datasets/new-york-city/nyc-rolling-sales) · [Bản lưu đối chiếu](https://github.com/varshabudihal/NYC_rolling_sales/blob/master/nyc-rolling-sales.csv)
- Để xác nhận **giấy phép và ghi công**, B đọc điều khoản trên nguồn phân phối đúng phiên bản, ghi tên giấy phép hoặc điều khoản, liên kết, cách ghi công, điều kiện chia sẻ lại và ngày truy cập. Hai đầu mối NYC và Kaggle chưa truy cập được từ máy đám mây khi soạn README, nên giấy phép, ngày công bố, đường tải gốc của đúng bản CSV và việc giảng viên duyệt vẫn cần được xác nhận. Hoàn tất các mục này trước khi chốt bộ dữ liệu hoặc phát hành bản nộp công khai. [Điều khoản NYC Open Data để đối chiếu](https://opendata.cityofnewyork.us/overview/)
- Trong notebook 01, xác định đối tượng được nguồn bao phủ, kiểu chuyển nhượng giá 0 hoặc giá danh nghĩa, cách nguồn xử lý diện tích trống và thời điểm các trường “AT PRESENT” được cập nhật. Mô tả lý do chọn dữ liệu và ảnh hưởng của hồ sơ thiếu thông tin, giao dịch lặp theo thửa và khoảng thời gian chỉ một năm.

| Notebook công khai đã xem | Nội dung liên quan và hướng đi riêng |
| --- | --- |
| Varsha Budihal dùng hồi quy tuyến tính và Random Forest với cách chia ngẫu nhiên train/test. | Q02 định nghĩa người dùng và thời điểm ước tính, chia theo thời gian và kiểm tra tài sản chưa từng thấy, so với mốc trung vị và báo cáo sai số theo nhóm. [NYC_Rolling_Sales_v1.ipynb](https://github.com/varshabudihal/NYC_rolling_sales/blob/master/NYC_Rolling_Sales_v1.ipynb) |
| Areeg Tarek khảo sát dữ liệu 2020–2022, kiểm định chênh lệch trước/sau COVID-19 và giữa Manhattan với phần còn lại. | Đồ án dùng giai đoạn 2016–2017, tập trung vào thay đổi cơ cấu loại nhà, giá theo diện tích, độ bất định và độ nhạy. [NYC_Rolling_Sales.ipynb](https://github.com/areegtarek/NYC-Rolling-Sales/blob/main/NYC_Rolling_Sales.ipynb) |

### Từ điển cột cần thống nhất

Dùng tên `snake_case` trong dữ liệu xử lý. Ghi tên gốc, tên mới, ý nghĩa, kiểu, đơn vị, quy tắc làm sạch và khả năng dùng ở thời điểm ước tính trong notebook 01.

| Nhóm | Cột gốc tiêu biểu | Dùng trong dự án |
| --- | --- | --- |
| Thời gian và mục tiêu | `SALE DATE`, `SALE PRICE` | Ngày giao dịch, giá bằng USD danh nghĩa. Dùng ngày để chia tập và tổng hợp theo thời gian. |
| Vị trí | `BOROUGH`, `NEIGHBORHOOD`, `ZIP CODE` | Borough và khu phố là danh mục. Mã ZIP lưu dưới dạng chuỗi để giữ số 0 đầu, nếu có. |
| Thửa và căn | `BLOCK`, `LOT`, `ADDRESS`, `APARTMENT NUMBER` | Ghép borough–block–lot để nhận diện thửa khi đủ cả ba trường. Dùng địa chỉ và căn để kiểm tra bản ghi nghi trùng. |
| Đặc tính | `BUILDING CLASS CATEGORY`, `YEAR BUILT`, `GROSS SQUARE FEET`, `LAND SQUARE FEET`, các cột `UNITS` | Loại công trình, năm xây, diện tích sàn/đất (ft²), số đơn vị ở/thương mại. Xác minh ý nghĩa và thời điểm có dữ liệu trước khi dùng làm đặc trưng. |
| Phân loại hành chính | `TAX CLASS …`, `BUILDING CLASS …` | Giữ riêng phiên bản hiện tại và phiên bản tại giao dịch để tránh gộp hai trường có ý nghĩa thời gian khác nhau. |
| Cột kỹ thuật | Cột đầu không tên và `EASE-MENT` | Cột đầu là ứng viên bỏ sau khi xác nhận ý nghĩa. `EASE-MENT` trống trên toàn bộ CSV hiện tại. |

## Câu hỏi và phương pháp đề xuất

Tập trọng tâm của Q01–Q04 và Q06 là giao dịch có giá dương, loại nhà một đến ba hộ (mã `01`, `02`, `03`). Xác minh mã với tài liệu nguồn. Tập có giá dương vẫn có thể chứa chuyển nhượng danh nghĩa. Ghi số dòng và kiểm tra độ nhạy theo quy tắc đã chốt. Q05 bắt đầu từ toàn bộ bản ghi thuộc ba loại nhà để kiểm tra tác động của chính các bộ lọc đó.

| Mã | Chủ câu | Câu hỏi và người dùng | Cách trả lời dự kiến |
| --- | --- | --- | --- |
| Q01 | A | Giá trung vị của nhà một đến ba hộ thay đổi thế nào giữa các kỳ ba tháng, và mức thay đổi còn bao nhiêu khi giữ cơ cấu borough × loại nhà cố định? Người đọc là người theo dõi xu hướng thị trường. | **D2, D4, D6.** Dùng bốn kỳ 09–11/2016, 12/2016–02/2017, 03–05/2017, 06–08/2017. Tính trung vị chung và chỉ số cơ cấu cố định, lấy tổng có trọng số của các trung vị theo tầng, chia cho giá trị tương ứng ở kỳ đầu rồi nhân 100. Trọng số là tỷ lệ số giao dịch từng tầng trong kỳ đầu, chuẩn hóa trên các tầng đủ mẫu ở cả bốn kỳ. Báo độ phủ và chạy lại với ngưỡng giá danh nghĩa khác. Vẽ đường xu hướng chung/chỉ số và đồ thị mức thay đổi theo tầng. |
| Q02 | A | Với nhà một đến ba hộ thuộc thửa chưa xuất hiện trong lịch sử huấn luyện, người mua có thể ước tính giá giao dịch tương lai tốt hơn mốc trung vị lịch sử bao nhiêu bằng thông tin có trước giao dịch? | **ML.** Dự đoán giá USD. So `DummyRegressor(strategy="median")`, `Ridge` và `RandomForestRegressor`, dùng pipeline và kiểm định theo thời gian. Vẽ giá dự đoán so với giá thật và sai số theo nhóm. Quy trình chi tiết ở dưới. |
| Q03 | B | Trong cùng loại nhà, chênh lệch trung vị giá trên ft² giữa mỗi borough và Queens lớn đến đâu, với độ bất định bao nhiêu? Người mua dùng kết quả để hiểu khác biệt theo vị trí. | **D3, D4, D5.** Tính USD/ft² trên diện tích sàn dương. So trong từng loại nhà, báo chênh lệch trung vị cùng khoảng tin cậy bootstrap percentile 95%. Dự kiến 2.000 lượt với seed 42, lấy mẫu theo thửa trong mỗi nhóm khi có giao dịch lặp. Ghi số thửa và cách xử lý khóa thiếu. Vẽ phân phối theo nhóm và đồ thị chênh lệch kèm khoảng tin cậy. |
| Q04 | B | Với nhà một hộ, chênh lệch giá giữa nhà xây trước 1940 và nhà xây từ 1980 trở đi thay đổi thế nào khi so trong cùng borough và cùng khoảng diện tích sàn? Người mua dùng kết quả để cân nhắc tuổi nhà và kích thước. | **D3, D4, D6.** Tạo nhóm năm xây và khoảng diện tích, dự kiến các khoảng dưới 1.000, 1.000–dưới 1.500, 1.500–dưới 2.000 và từ 2.000 ft². Công bố ngưỡng trước khi so giá. So trung vị trong các tầng có ít nhất 20 giao dịch ở mỗi nhóm năm xây, rồi báo số dòng và số tầng đủ mẫu. Lặp với cách chia diện tích hoặc mốc năm khác. Vẽ chênh lệch chung/đã phân tầng và số dòng theo tầng. |
| Q05 | C | Điều kiện có giá và diện tích hợp lệ giữ lại bao nhiêu giao dịch ở mỗi borough và loại nhà? Người đọc cần biết các so sánh giá/ft² đại diện cho phần nào của dữ liệu ban đầu. | **D4, D5, D6.** Dùng toàn bộ bản ghi của ba loại. Báo tỷ lệ qua từng bộ lọc theo tầng và khoảng tin cậy bootstrap 95% theo thửa khi phù hợp. So điều kiện giá dương với một ngưỡng nhạy cảm và đối chiếu số dòng. Vẽ phễu theo bước và heatmap tỷ lệ giữ lại. |
| Q06 | C | Trong từng loại nhà, 10% giao dịch đắt nhất chiếm bao nhiêu phần trăm tổng giá trị ở mỗi borough, và mức tập trung thay đổi thế nào khi bỏ nhóm 1% giá cao nhất? Người đọc dùng kết quả để đánh giá vai trò của giao dịch cực lớn. | **D3, D4, D6.** Tính tỷ trọng giá trị từ top 10% theo từng tầng borough × loại nhà; ghi cách làm tròn lượng bản ghi và xử lý đồng hạng. Lặp sau khi bỏ top 1% ở từng tầng và tính lại mẫu số. Vẽ tỷ trọng theo nhóm và mức thay đổi giữa hai kịch bản. |

Với Q01–Q04, nhóm đã có phương án phủ **D2, D3, D4, D5, D6** thông qua ba câu phân tích. D1 chỉ tính khi thực sự ghép thêm một bảng và báo số dòng trước/sau, khóa trùng, số khóa không ghép được và lý do ghép. Các so sánh đều mang tính mô tả. Với tầng ít quan sát, báo cỡ mẫu và giới hạn suy luận thay vì rút kết luận mạnh.

### Thiết kế Q02 để nhóm triển khai

1. **Chọn đặc trưng sẵn có trước giao dịch.** Người mua biết vị trí và thông tin tài sản có sẵn trước giao dịch. Khởi đầu với borough/khu phố. Thêm năm xây, diện tích và loại nhà vào đặc trưng khi có căn cứ về thời điểm các trường đó sẵn có. Ghi rõ phạm vi hồi cứu của mẫu nếu loại nhà chỉ có thể xác định từ bản ghi lịch sử. Loại khỏi `X` giá bán, biến dẫn xuất từ giá, ngày bán thực tế, trường phân loại tại giao dịch/hiện tại chưa xác nhận thời điểm và khóa thửa. Giữ ngày để chia tập và khóa thửa để kiểm tra nhóm.
2. **Chia tập trước khi huấn luyện.** Dự kiến train **09/2016–05/2017**, test **06–08/2017**. Phạm vi đánh giá chính là các thửa đủ khóa và chưa xuất hiện trong train. Báo số dòng thiếu khóa, số thửa đã thấy, số dòng giữ lại và xác nhận hai tập đánh giá không trùng thửa. Trong train, dùng các fold cửa sổ mở rộng theo tháng với validation ở tháng sau. Trong mỗi fold, chỉ chấm các thửa chưa xuất hiện trong phần train của fold đó. In khoảng ngày và cỡ mẫu từng fold, dùng cùng các fold cho cả ba phương án.
3. **Dựng pipeline và tinh chỉnh trên train.** Dùng `ColumnTransformer` cho danh mục và số, `SimpleImputer` trong pipeline nếu cần, `OneHotEncoder(handle_unknown="ignore")` cho danh mục và scale cột số khi mô hình cần. Baseline lấy trung vị `y` của train. Chọn tham số của Ridge và Random Forest bằng CV chỉ trên train. Đặt `random_state=42` cho bước có ngẫu nhiên. Đóng băng cấu hình sau CV rồi fit lại trên toàn bộ train.
4. **Đo sai số và giải thích mô hình.** Dùng **MAE (USD)** làm chỉ số chính vì đo trực tiếp sai số tuyệt đối trung bình theo đơn vị tiền. Báo thêm RMSE để thấy ảnh hưởng của lỗi rất lớn. Báo bảng CV rồi chạy một lượt đánh giá test cuối cho các phương án đã cố định. Dùng cùng mẫu test để so mức cải thiện so với baseline. Phân tích phần dư theo borough, loại nhà và nhóm giá có ngưỡng xác định từ train. Dùng permutation importance trên một fold validation theo thời gian để giải thích mô hình. Báo điều kiện mô hình thất bại và đối tượng có thể sử dụng.

## Quy trình dữ liệu và thao tác code

| Thứ tự | Nơi thực hiện | Đầu ra cần có |
| --- | --- | --- |
| 1. Thu thập | [Notebook 01](notebooks/01_collection_exploration.ipynb) | Nguồn, quyền sử dụng, bản tải, bối cảnh, đối tượng và phương pháp thu thập. |
| 2. Khám phá | Notebook 01 | Kích thước, từ điển cột, số và tỷ lệ thiếu, dòng nghi trùng, phân phối và ngoại lệ, nhãn hiếm, tương quan/cross-tab cần thiết. Chốt 3–5 quan sát gợi dẫn đến câu hỏi. |
| 3. Chốt câu hỏi và chuẩn hóa | Notebook 01 và mã dùng chung trong `src/` khi có nhu cầu | Một bảng chuẩn hóa tái lập được, dự kiến `data/processed/nyc_sales_clean.csv`, cùng bảng kiểm tra số dòng. Tách các bộ lọc riêng của từng câu ra khỏi bước dùng chung. |
| 4. Trả lời câu hỏi | [Notebook 02](notebooks/02_analysis.ipynb) và [Notebook 03](notebooks/03_ml_question.ipynb) | Notebook 02 làm Q01, Q03, Q04 (thêm Q05, Q06 nếu có). Notebook 03 làm Q02. Nếu nhiều người cần viết đồng thời, tách notebook 02 theo mã câu như `02_Q03_price_per_sqft.ipynb` và cập nhật thứ tự chạy ở README. |
| 5. Tổng kết | Cuối Notebook 02, README và [slide](slides.pdf) | Bảng kết quả, 3–5 phát hiện chính, giới hạn, hướng phát triển và phản ánh do từng thành viên viết. |

### Quy tắc làm sạch và kiểm tra

1. **Nạp và xác nhận schema.** Giữ CSV gốc trong `data/raw/` và đọc dữ liệu dạng chuỗi khi cần giữ mã. Xác nhận số cột, độ phủ thời gian và giá trị mã. Đổi tên cột nhất quán, bỏ khoảng trắng dư, xử lý chuỗi rỗng và ký hiệu `-` theo từng cột. CSV hiện tại có 14.561 giá ghi `-` và 10.228 giá ghi `0` sau khi bỏ khoảng trắng; notebook cần kiểm lại hai nhóm riêng.
2. **Ép kiểu có kiểm tra.** Chuyển ngày bằng pandas, chuyển giá/diện tích về số và thống kê số lỗi ép kiểu. Năm xây `0`, ZIP `0`, diện tích `0` và giá `0` có ý nghĩa khác nhau. Giữ cờ để phân biệt số 0 gốc với giá trị thiếu trước khi lọc hoặc điền. Với biến dẫn xuất, xác minh miền giá trị và đơn vị.
3. **Kiểm tra giao dịch trùng.** Phân biệt dòng giống hệt sau khi bỏ chỉ số xuất tệp với các giao dịch khác ngày/giá của cùng thửa. So thêm căn, địa chỉ và mã phân loại khi cần. Ghi quy tắc giữ hoặc gộp dòng và số lượng chịu ảnh hưởng. Dùng khóa ghép dưới dạng chuỗi để so tập train/test hoặc bootstrap theo thửa; kiểm tra số dòng thiếu khóa.
4. **Tách dữ liệu theo mục tiêu phân tích.** Giữ các trường hợp giá 0 hoặc thiếu để mô tả độ phủ; dùng tập giá dương cho phân tích giá. Chỉ yêu cầu diện tích dương khi tính USD/ft² hoặc chia theo diện tích. Báo `n` và tỷ lệ mất dữ liệu theo borough × loại nhà. Thử một quy tắc hợp lý khác cho giá danh nghĩa hoặc ngoại lệ, ghi rõ ngưỡng và lý do trước khi so kết quả.
5. **Ghi sổ kiểm tra trong notebook.** Trước và sau mỗi bước lọc, bỏ hoặc ghép, ghi tên bước, số dòng trước/sau, chênh lệch và lý do. Với phép ghép, chốt số lượng khóa kỳ vọng, dùng `validate=` phù hợp của pandas, đếm khóa không khớp và kiểm tra hiện tượng nhân dòng. Kiểm tra đầu ra có schema và số dòng mong đợi trước khi ghi vào `data/processed/`. Với CSV xử lý, lưu ngày dạng ISO và thống nhất kiểu khi đọc lại, nhất là ngày và các mã dạng chuỗi.

### Cách tổ chức và trình bày code

- Chạy Jupyter Notebook từ thư mục gốc. Trong notebook, xác định thư mục gốc bằng `pathlib.Path` từ thư mục hiện tại hoặc cha của nó và kiểm tra thấy `environment.yml` trước khi dựng đường dẫn. Dùng `data/raw/` cho đầu vào, `data/processed/` cho đầu ra tạo lại được. Giữ đường dẫn máy cá nhân ngoài notebook.
- Đặt cell import, đường dẫn, seed và cấu hình ở đầu. Đặt tên biến/hàm Python bằng tiếng Anh, `snake_case`, và kèm đơn vị trong tên khi hữu ích như `sale_price_usd` hoặc `gross_sqft`. Đặt một chức năng rõ ràng cho mỗi cell; chỉ chuyển logic lặp lại sang `src/` khi đã có quy tắc chung được review.
- Mỗi câu bắt đầu bằng **mã, chủ câu và câu hỏi**, sau đó trình bày động cơ và người dùng, mẫu và làm sạch, phương pháp và tiêu chí, kết quả, câu trả lời và giới hạn. Mỗi bước tiền xử lý có câu giải thích trước cell code. Mỗi kết quả chính ghi nhóm, giai đoạn, cỡ mẫu, giá trị và đơn vị.
- Biểu đồ dùng tiếng Việt nhất quán, có tiêu đề, tên trục, đơn vị và chú giải khi có nhiều nhóm. Cố định thứ tự và màu borough giữa các notebook, dùng thang đo giống nhau khi so trực tiếp, ghi rõ trục log nếu dùng. Dưới biểu đồ ghi phạm vi, `n` và một nhận xét dựa trên số liệu. Mỗi câu có ít nhất hai biểu đồ phục vụ hai ý đọc khác nhau.
- Khởi động lại kernel và chạy `Run All` sau khi sửa. Giữ phần xuất cần đọc, cắt bảng dài và rà dữ liệu hiển thị. Với code dùng ngẫu nhiên, đặt seed. Giữ output từ lần chạy cuối nhất quán với bảng README và slide.

## Cài đặt và chạy lại

### 1. Lấy repo và kiểm tra nhánh

```bash
git clone --branch vnhatminh https://github.com/minhvonhat/Data-Science-Final-Project.git
cd Data-Science-Final-Project
git status -sb
```

Trong Codex Cloud, dùng checkout có sẵn tại `/workspace/Data-Science-Final-Project` và kiểm tra bằng `git branch --show-current`.

### 2. Cài Miniconda và tạo môi trường

Tải bộ cài Miniconda phù hợp với hệ điều hành và kiến trúc máy. Sau khi cài, mở **Miniconda Prompt** hoặc **Anaconda Prompt** trên Windows, hoặc mở lại Terminal trên macOS/Linux. Chạy `conda --version` để kiểm tra trước khi vào thư mục gốc của repo. [Bộ cài Miniconda](https://repo.anaconda.com/miniconda/)

Dùng Miniconda để tạo môi trường Python 3.11, rồi cài Jupyter Notebook và các thư viện phân tích bằng `pip` bên trong môi trường đó. Cách này dùng các phiên bản thư viện phân tích đã ghi trong cấu hình dự án, kể cả những phiên bản hiện thiếu trên kênh Conda `defaults`. [Cấu hình môi trường](environment.yml)

```bash
conda create -n min_ds-env python=3.11 pip
conda activate min_ds-env
python -m pip install notebook==7.0.8
python -m pip install numpy==1.26.0 pandas==2.1.1 scipy==1.11.3 matplotlib==3.8.0 seaborn==0.13.0 scikit-learn==1.3.1
python --version
jupyter notebook --version
```

Nếu đã có môi trường `min_ds-env` chạy Python 3.11, bắt đầu từ `conda activate min_ds-env`. Những lần sau, chỉ cần kích hoạt lại môi trường khi mở terminal mới. Khi notebook có thêm yêu cầu, kiểm tra phiên bản tương ứng trong `environment.yml` trước khi cài gói bổ sung.

Trên Codex Cloud đã thiết lập, dùng `.venv` có sẵn từ thư mục repo. Khi cần tạo lại, dùng script cài đặt trong cấu hình môi trường. Đoạn lệnh dưới đây áp dụng cho Cloud.

```bash
source .venv/bin/activate
export JUPYTER_CONFIG_DIR="$VIRTUAL_ENV/jupyter/config"
export JUPYTER_RUNTIME_DIR="$VIRTUAL_ENV/jupyter/runtime"
export IPYTHONDIR="$VIRTUAL_ENV/ipython"
export MPLCONFIGDIR="$VIRTUAL_ENV/cache/matplotlib"
export XDG_CACHE_HOME="$VIRTUAL_ENV/cache"
mkdir -p "$JUPYTER_CONFIG_DIR" "$JUPYTER_RUNTIME_DIR" "$IPYTHONDIR" "$MPLCONFIGDIR"
python --version
jupyter notebook --version
```

### 3. Chuẩn bị dữ liệu

CSV hiện có sẵn trong checkout. Nếu thiếu, xác nhận quyền truy cập và tải đúng bản lịch sử từ Kaggle, rồi giải nén `nyc-rolling-sales.csv` vào `data/raw/`. Có thể dùng lệnh dưới đây khi đã cài Kaggle CLI và đăng nhập bằng phương thức của Kaggle. Giữ tệp thông tin đăng nhập ngoài repo. [Kaggle NYC Rolling Sales](https://www.kaggle.com/datasets/new-york-city/nyc-rolling-sales)

```bash
mkdir -p data/raw data/processed
kaggle datasets download new-york-city/nyc-rolling-sales -p data/raw --unzip
```

Kiểm tra tệp hiện có trước khi chạy. SHA-256 kỳ vọng của bản đã đối chiếu là `97228c77c1558c70cac0d8949556fd6dc43d70d8deebc66d6333d76e5ee817be`. Nếu bản tải có hash khác, xác minh bộ cột, khoảng ngày, số dòng và xuất xứ trước khi dùng vì các bản xuất có thể khác định dạng hoặc kỳ báo cáo.

```bash
python - <<'PY'
from hashlib import sha256
from pathlib import Path

import pandas as pd

path = Path("data/raw/nyc-rolling-sales.csv")
assert path.is_file(), f"Missing: {path}"
raw = pd.read_csv(path)
assert raw.shape == (84_548, 22), raw.shape
assert {"SALE DATE", "SALE PRICE", "BOROUGH"} <= set(raw.columns)
print("Shape:", raw.shape)
print("SHA-256:", sha256(path.read_bytes()).hexdigest())
PY
```

Đề bài yêu cầu giữ tệp dữ liệu lớn ngoài Git. Bản CSV khoảng 13 MB đã được theo dõi trong lịch sử của repo. Nhóm giữ nguyên hiện trạng trong lần cập nhật README và cần thống nhất với giảng viên cách bàn giao CSV sau khi xác minh điều khoản. Với tệp đầu vào tải thêm và đầu ra sinh lại, giữ theo quy tắc ignore của repo và chỉ commit mã, notebook, tài liệu hoặc mẫu nhỏ có lý do rõ ràng.

### 4. Mở Jupyter Notebook

Từ thư mục gốc của repo, chạy lệnh sau trong terminal đã kích hoạt môi trường.

```bash
jupyter notebook
```

Trên máy cá nhân, Jupyter sẽ mở trang danh sách tệp trong trình duyệt. Nếu trình duyệt chưa mở, dùng địa chỉ Jupyter in trong terminal. Trên Codex Cloud, dùng `jupyter notebook --no-browser` để khởi động từ terminal. Vào thư mục `notebooks/` để mở tệp.

Chọn kernel **Python 3 (ipykernel)** thuộc môi trường vừa kích hoạt. Mở **01 → 02 → 03**, dùng **Restart Kernel and Run All Cells** cho từng notebook. Khi các bước triển khai đã có code, kiểm tra notebook 01 tạo đầu ra đã thống nhất, 02 đọc đầu ra đó để tái tạo các bảng và biểu đồ, và 03 tái tạo bảng CV, kết quả test cùng đồ thị phân tích lỗi. Nếu đổi kernel, xác nhận `sys.executable` là Python của môi trường dự án. Nếu lỗi đường dẫn, kiểm tra thư mục làm việc và đúng tên tệp trước khi sửa code.

Hiện tại các notebook chỉ có đề mục Markdown. Kiểm tra môi trường đã đọc được CSV, mở được trang danh sách tệp của Jupyter Notebook và chạy được một notebook tạm với pandas, biểu đồ và scikit-learn. Đây là kiểm tra công cụ và đầu vào. Các câu hỏi nghiên cứu sẽ có kết quả sau khi nhóm triển khai và chạy quy trình phân tích.

## Làm việc bằng Git

`vnhatminh` là nhánh tích hợp hiện tại. Mỗi chủ câu tạo nhánh công việc từ phiên bản mới nhất của nhánh tích hợp. Đoạn lệnh dưới đây dùng Q03 làm ví dụ.

```bash
git switch vnhatminh
git pull --ff-only origin vnhatminh
git switch -c q03-gia-theo-dien-tich

# Sau khi chỉnh và chạy notebook, chỉ stage những tệp thuộc câu hỏi.
git status --short
git diff --stat
git add notebooks/02_analysis.ipynb
git diff --cached --stat
git commit -m "Analyze sale price per square foot for Q03"
git push -u origin q03-gia-theo-dien-tich
```

1. Tạo issue hoặc ghi việc cần làm với mã câu, người phụ trách, file sẽ sửa, đầu vào, đầu ra và tiêu chí hoàn thành. Thống nhất trước khi sửa file dùng chung, nhất là notebook 01 và schema bảng xử lý.
2. Mở pull request với đích `vnhatminh`. Ghi câu hỏi, thay đổi phương pháp/tiền xử lý, cách chạy, số dòng trước/sau, đồ thị hoặc bảng đầu ra và việc còn thiếu. Mỗi commit tập trung vào một thay đổi để Git thể hiện đóng góp của từng người.
3. Người review chạy lại phần liên quan, kiểm tra dữ liệu, nhãn và kết luận. Khi hai nhánh cùng sửa notebook, ưu tiên tách phần theo mã câu hoặc dùng `nbdime` để đọc khác biệt. Người sở hữu các cell liên quan thống nhất nội dung sau khi giải xung đột, rồi chạy lại notebook trước khi merge.
4. Sau merge, mọi người cập nhật nhánh tích hợp bằng `git pull --ff-only origin vnhatminh`. Giữ lịch sử nhánh chung theo cách tích hợp đã thống nhất. Trước khi nộp, một thành viên khác chạy toàn bộ quy trình từ checkout sạch và đối chiếu số liệu với README, slide.

## Tiến độ, kết quả và trình bày

T là hạn nộp do giảng viên công bố. Các mốc dưới đây là kế hoạch nội bộ đề xuất. Nếu lịch ngắn hơn, giữ thứ tự và hoàn tất duyệt dữ liệu trước khi chốt câu hỏi.

| Mốc | Chủ trì | Đầu ra để chuyển bước |
| --- | --- | --- |
| T − 14 ngày | Cả nhóm, B theo dõi | Tên/MSSV, quy mô nhóm, nguồn và giấy phép đúng phiên bản, danh mục công trình liên quan, xác nhận duyệt dữ liệu. |
| T − 11 ngày | B và chủ câu | Notebook 01 có EDA, sổ số dòng, từ điển cột; chốt các câu, tập áp dụng, tiêu chí độ sâu và ngưỡng kiểm tra. |
| T − 7 ngày | Từng chủ câu | Có nhánh và PR theo câu; 02 có bảng/biểu đồ sơ bộ, 03 có baseline, split và CV. Review mẫu và đối chiếu kết quả. |
| T − 4 ngày | A và người review | Hoàn thành đánh giá, kiểm tra độ nhạy, chạy lại từ checkout sạch, chốt 3–5 phát hiện và giới hạn. |
| T − 2 ngày đến T | C hoặc B, cùng cả nhóm | Sửa README, cập nhật nhật ký, hoàn tất phản ánh cá nhân, xuất PDF slide, tập trình bày và chuẩn bị hỏi đáp. |

### Cách ghi kết quả cuối

Sau khi review, thêm bảng kết quả ở đây với **mã câu, mẫu/giai đoạn, số liệu chính và đơn vị, kết luận, giới hạn, notebook chứa bằng chứng**. Tóm tắt 3–5 phát hiện cho cả dự án và làm nổi bật phát hiện bất ngờ nhất. Hiện repo có số liệu kiểm tra đầu vào, còn các kết luận thực nghiệm của Q01–Q06 đang chờ triển khai.

### Dàn ý slide và hỏi đáp

- Dành **2 phút** cho bối cảnh, người dùng kết quả, dữ liệu, phạm vi và câu hỏi. Thay bìa mẫu bằng tên đồ án, họ tên/MSSV và chủ đề.
- Dành **10 phút** để các thành viên trình bày câu mình sở hữu. Mỗi câu chọn hình trả lời trực tiếp, đọc con số và giới hạn. Q02 nêu rõ mốc baseline, cách chia theo thời gian và sai số ngoài mẫu.
- Dành **3 phút** để nêu 3–5 phát hiện, phát hiện bất ngờ, giới hạn, hướng phát triển và cách tái lập.
- Trong **10 phút hỏi đáp**, mỗi người chuẩn bị giải thích nguồn/giấy phép, lý do lọc và số dòng thay đổi, lựa chọn D1–D6, dữ liệu sẵn có tại thời điểm dự đoán, cách chia tập, chỉ số và bằng chứng. Tập giải thích cả code do thành viên khác viết.

### Nhật ký học thuật và rà soát trước nộp

- Mỗi thành viên tự viết code phân tích, câu trả lời và phản ánh. Dùng LLM để học khái niệm, đọc lỗi và hiểu API theo quy định môn học. Mỗi lần dùng đáng kể cập nhật công cụ, câu hỏi, cách dùng hoặc chỉnh sửa trong [`LLM_USAGE.md`](LLM_USAGE.md). Ghi nguồn cho đoạn trích, ý tưởng và đoạn mã tham khảo.
- [ ] Điền thông tin nhóm, kiểm tra đúng hai câu mỗi người, xác nhận dữ liệu và điều khoản.
- [ ] Mỗi câu phân tích có ít nhất hai tiêu chí độ sâu, cả nhóm phủ ít nhất bốn tiêu chí. Kiểm tra hai biểu đồ mỗi câu, số dòng, đơn vị, nhóm so sánh và giới hạn.
- [ ] Xác nhận split, baseline, hai mô hình, pipeline, CV trên train, đánh giá test, phân tích lỗi và diễn giải Q02.
- [ ] Tái lập từ đầu, đối chiếu kết quả notebook/README/slide, ghi đủ nhật ký LLM, tệp nộp và phản ánh cá nhân.
- [ ] Mọi thành viên tập trình bày và hỏi đáp. Kiểm tra link GitHub, file PDF, nhánh nộp và hạn do giảng viên công bố.
