# Đề xuất Bộ 6 Câu hỏi Nghiên cứu & Lộ trình Triển khai
**Bộ dữ liệu:** UK Car Accidents 2005–2015 (`dft-accident-data` — STATS19)

Bộ câu hỏi dưới đây được thiết kế bám sát cấu trúc thư mục `notebooks/` hiện có của dự án, giải quyết các bài toán quản lý an toàn giao thông thực tế tại Vương quốc Anh, đồng thời đáp ứng trọn vẹn **6/6 tiêu chí chiều sâu (D1–D6)** cho nhóm câu hỏi phân tích và **6/6 yêu cầu bắt buộc** cho phần Machine Learning.

---

## Tổng quan mức độ bao phủ tiêu chí đề bài

| Câu hỏi & File Notebook | Trọng tâm bài toán thực tế | Tiêu chí đạt được |
| :--- | :--- | :--- |
| **Q1** (`02_q01_xu_huong.ipynb`) | Xu hướng mức độ nghiêm trọng & nghịch lý loại đường / tốc độ | **D1, D2, D3, D4** |
| **Q2** (`02_q03_thuong_tich.ipynb`) | Rủi ro tử vong của nhóm dễ tổn thương & hướng va chạm | **D1, D3, D4, D5** |
| **Q3** (`02_q04_anh_sang.ipynb`) | Hiệu quả đèn đường ban đêm & bài toán tắt đèn tiết kiệm điện | **D2, D3, D4, D5, D6** |
| **Q4** (`02_q05_do_phu.ipynb`) | Mặt đường bất lợi, hiện tượng trượt/lật xe & phân hóa vùng miền | **D1, D3, D4, D6** |
| **Q5** (`02_q06_so_nguoi_bi_nan.ipynb`) | Quy mô thương vong & bất bình đẳng kinh tế – xã hội (IMD) | **D1, D2, D3, D4, D5** |
| **Q6** (`03_ml_question.ipynb`) | Dự đoán sớm ca nguy kịch (`KSI`) hỗ trợ điều phối cấp cứu 999 | **Đủ 6/6 mục ML** |

---

## Phần 1: 5 Câu hỏi Phân tích Chuyên sâu (Non-ML Questions)

### Câu 1 (`02_q01_xu_huong.ipynb`): Xu hướng mức độ nghiêm trọng và "điểm mù chết người" theo loại đường

* **Câu hỏi nghiên cứu:**
  > Trong giai đoạn 2005–2015, dù tổng số vụ tai nạn tại Anh giảm mạnh, tỷ lệ tai nạn nghiêm trọng ($\text{KSI\_Rate}$) biến động ra sao theo thời gian, và sự đối lập giữa mức độ va chạm liên hoàn (số phương tiện/vụ) với tỷ lệ tử vong trên mỗi phương tiện giữa các loại đường (`Road_Type`) có giữ nguyên sau khi kiểm soát giới hạn tốc độ (`Speed_limit`) và khu vực đô thị/nông thôn (`Urban_or_Rural_Area`) hay không?

* **Động lực & Giá trị ra quyết định (Motivation):**
  * **Đối tượng hưởng lợi:** Bộ Giao thông vận tải Anh (DfT), hội đồng quy hoạch hạ tầng địa phương và doanh nghiệp bảo hiểm xe cơ giới.
  * **Quyết định thực tế:** Giúp phân bổ ngân sách an toàn giao thông đúng trọng tâm — ưu tiên **cải tạo hình học nút giao/vòng xuyến** ở các tuyến nội đô va chạm nhiều xe nhưng nhẹ, và **hạ giới hạn tốc độ / lắp camera phạt nguội** tại đường hai chiều nông thôn (`Single carriageway`, $60\text{ mph}$) nơi ít va chạm liên hoàn nhưng tỷ lệ chết người cao nhất.

* **Lộ trình triển khai đạt tiêu chí:**
  * **D1 (Combining data):** Sử dụng bảng ghép `accident_counts.csv` (tổng hợp từ `Accidents`, `Vehicles`, `Casualties`), kiểm chứng số dòng khớp khóa và ánh xạ nhãn từ `contextCSVs/Road_Type.csv`.
  * **D2 (Reshaping & time):** Gom dữ liệu theo tháng (`resample`), dùng `pivot` tách cột theo 3 mức độ (`Fatal`, `Serious`, `Slight`), tính trung bình trượt 12 tháng (`rolling`) và tỷ lệ tăng/giảm cùng kỳ năm trước (YoY).
  * **D3 (Derived variables):** Xây dựng các biến chuẩn hóa:
    $$\text{KSI\_Rate} = \frac{\text{Số vụ Fatal} + \text{Số vụ Serious}}{\text{Tổng số vụ tai nạn}} \times 100\%$$
    $$\text{Vehicles\_per\_Accident} = \frac{\text{Tổng số phương tiện}}{\text{Tổng số vụ tai nạn}}, \quad \text{Casualties\_per\_Vehicle} = \frac{\text{Tổng số nạn nhân}}{\text{Tổng số phương tiện}}$$
  * **D4 (Controlling for a confounder):** Phân tầng đối chiếu theo `Speed_limit` ($30\text{ mph}$ so với $60\text{ mph}$) và `Urban_or_Rural_Area`.

---

### Câu 2 (`02_q03_thuong_tich.ipynb`): Mức độ tổn thương của nhóm yếu thế và tác động của hướng va chạm

* **Câu hỏi nghiên cứu:**
  > Sau khi kiểm soát giới hạn tốc độ và nhóm tuổi nạn nhân, người tham gia giao thông dễ tổn thương (xe máy, xe đạp, người đi bộ) chịu tỷ lệ thương vong nghiêm trọng ($\text{KSI\_Share}$) cao hơn người ngồi trong ô tô bao nhiêu lần, và điểm va chạm đầu tiên (`1st_Point_of_Impact`) hay thao tác lái (`Vehicle_Manoeuvre`) nào làm tăng đột biến nguy cơ tử vong?

* **Động lực & Giá trị ra quyết định (Motivation):**
  * **Đối tượng hưởng lợi:** Cơ quan thiết kế hạ tầng đô thị, tổ chức vận động an toàn cho người đi xe đạp/đi bộ và các công ty bảo hiểm.
  * **Quyết định thực tế:** Xác định các tình huống xung đột giao thông nguy hiểm nhất (như ô tô rẽ phải cắt ngang làn xe hai bánh) để thiết kế làn đường tách biệt, đèn tín hiệu ưu tiên và giải phân cách bảo vệ nhóm yếu thế.

* **Lộ trình triển khai đạt tiêu chí:**
  * **D1 (Combining data):** Sử dụng bảng ghép $N:1$ `casualty_vehicle.csv` kết hợp với `accidents_clean.csv` và các bảng giải mã `Casualty_Type.csv`, `Vehicle_Type.csv`, `1st_Point_of_Impact.csv`.
  * **D3 (Derived variables):** Phân nhóm đối tượng thành *Vulnerable Road Users (VRU)* so với *Car Occupants* và tính tỷ lệ $\text{KSI\_Share}$ trên từng tổ hợp va chạm.
  * **D4 (Controlling for a confounder):** Kiểm soát `Speed_limit` và `Age_Band_of_Casualty` (tách riêng nhóm người cao tuổi vốn có thể trạng dễ chấn thương nặng hơn).
  * **D5 (Quantifying uncertainty):** Tính khoảng tin cậy $95\%$ (Bootstrap CI) cho chênh lệch $\text{KSI\_Share}$ và thực hiện kiểm định Chi-square kèm hệ số độ lớn tác động (Cramér's V / Odds Ratio).

---

### Câu 3 (`02_q04_anh_sang.ipynb`): Hiệu quả đèn chiếu sáng ban đêm và chính sách tiết kiệm điện đô thị

* **Câu hỏi nghiên cứu:**
  > Tỷ lệ tai nạn nghiêm trọng ($\text{KSI\_Rate}$) vào ban đêm không có đèn đường (`Darkness - no street lighting`) cao hơn ban đêm có đèn đường và ban ngày bao nhiêu phần trăm sau khi kiểm soát yếu tố khu vực đô thị/nông thôn, giới hạn tốc độ và khung giờ khuya ($0\text{h}–4\text{h}$ sáng)?

* **Động lực & Giá trị ra quyết định (Motivation):**
  * **Đối tượng hưởng lợi:** Chính quyền địa phương (Local Councils) và đơn vị quản lý chiếu sáng công cộng.
  * **Quyết định thực tế:** Giải quyết trực tiếp bài toán tranh cãi tại Anh giai đoạn 2008–2015 về chính sách **tắt bớt đèn đường sau nửa đêm để tiết kiệm ngân sách và giảm phát thải**, giúp khoanh vùng chính xác các tuyến đường bắt buộc phải duy trì chiếu sáng để tránh gia tăng tai nạn chết người.

* **Lộ trình triển khai đạt tiêu chí:**
  * **D2 (Reshaping & time):** Trích xuất giờ từ cột `Time`, dùng `pivot` đối chiếu tỷ lệ $\text{KSI\_Rate}$ theo từng khung giờ trong ngày (đặc biệt là giờ cao điểm tối và đêm khuya).
  * **D3 (Derived variables):** Chuẩn hóa biến điều kiện ánh sáng thành 3 nhóm (*Daylight*, *Lit Darkness*, *Unlit Darkness*) và tính chỉ số $\text{KSI\_Rate}$.
  * **D4 (Controlling for a confounder):** Kiểm soát khung giờ $0\text{h}–4\text{h}$ sáng (nhằm tách bạch tác động của việc thiếu ánh sáng khỏi yếu tố tài xế buồn ngủ hoặc sử dụng rượu bia vào đêm muộn) cùng `Urban_or_Rural_Area`.
  * **D5 (Uncertainty):** Kiểm định Z-test hai tỷ lệ và tính khoảng tin cậy $95\%$ cho mức chênh lệch rủi ro giữa đường có đèn và không đèn.
  * **D6 (Robustness check):** Kiểm tra xem kết luận có thay đổi không nếu loại bỏ các khung giờ giao thời hoàng hôn/bình minh ($16\text{h}–18\text{h}$ mùa đông) hoặc tách riêng giai đoạn trước và sau năm 2010.

---

### Câu 4 (`02_q05_do_phu.ipynb`): Tình trạng mặt đường bất lợi, hiện tượng trượt/lật xe và sự phân hóa vùng miền

* **Câu hỏi nghiên cứu:**
  > Mặt đường ướt, đóng băng hoặc tuyết phủ (`Road_Surface_Conditions`) làm gia tăng tỷ lệ mất lái (trượt bánh/lật xe — `Skidding_and_Overturning`) và mức độ nghiêm trọng của tai nạn ra sao khi kiểm soát loại phương tiện (2 bánh so với 4 bánh) và vĩ độ địa lý (miền Bắc/Scotland lạnh giá so với miền Nam nước Anh)?

* **Động lực & Giá trị ra quyết định (Motivation):**
  * **Đối tượng hưởng lợi:** Cơ quan quản lý đường cao tốc (Highways England), đơn vị bảo trì mặt đường và trung tâm dự báo thời tiết giao thông.
  * **Quyết định thực tế:** Tối ưu hóa lịch trình rải muối chống đóng băng theo vĩ độ, nâng cấp độ nhám mặt đường thoát nước ở các điểm đen hay xảy ra trượt bánh và phát cảnh báo chuyên biệt cho người đi xe hai bánh.

* **Lộ trình triển khai đạt tiêu chí:**
  * **D1 (Combining data):** Ghép bảng `Vehicles0515.csv` (lấy `Skidding_and_Overturning`, `Vehicle_Type`) với `Accidents0515.csv` (lấy `Road_Surface_Conditions`, `Weather_Conditions`, `Latitude`).
  * **D3 (Derived variables):** Tạo biến cờ nhị phân `Is_Skid_Overturn` (có trượt/lật hay không) và biến phân vùng địa lý Bắc/Trung/Nam dựa trên vĩ độ `Latitude`.
  * **D4 (Controlling for a confounder):** Kiểm soát `Vehicle_Type` (xe máy dễ trượt ngã hơn ô tô trên đường ướt) và `Speed_limit`.
  * **D6 (Robustness check):** So sánh kết quả khi giữ nguyên toàn bộ dữ liệu với khi loại bỏ hai mùa đông băng tuyết kỷ lục tại Anh (2009–2010) để đảm bảo quy luật không bị bóp méo bởi biến cố thời tiết cực đoan.

---

### Câu 5 (`02_q06_so_nguoi_bi_nan.ipynb`): Quy mô thương vong và bất bình đẳng kinh tế – xã hội (IMD)

* **Câu hỏi nghiên cứu:**
  > Các vụ tai nạn xảy ra ở khu vực có mức độ thiếu thốn kinh tế – xã hội cao (`IMD_Decile` thấp) hoặc liên quan đến tài xế cư trú ở vùng khó khăn có xu hướng gây ra nhiều nạn nhân trên mỗi vụ ($\text{Casualties\_per\_Accident}$) và tỷ lệ trẻ em/người đi bộ bị nạn cao hơn khu vực khá giả hay không, và khoảng cách này có thu hẹp trong giai đoạn 2011–2015 không?

* **Động lực & Giá trị ra quyết định (Motivation):**
  * **Đối tượng hưởng lợi:** Hội đồng y tế công cộng (Public Health England) và chính quyền quy hoạch đô thị.
  * **Quyết định thực tế:** Chứng minh mối liên hệ giữa bất bình đẳng thu nhập và rủi ro tai nạn giao thông, từ đó ưu tiên ngân sách lắp đặt vạch sang đường, gờ giảm tốc và vùng giới hạn tốc độ $20\text{ mph}$ quanh trường học tại các khu dân cư thu nhập thấp.

* **Lộ trình triển khai đạt tiêu chí:**
  * **D1 (Combining data):** Ghép cả 3 bảng `Accidents`, `Casualties` (lấy `Casualty_IMD_Decile`, `Age_of_Casualty`, `Casualty_Type`) và `Vehicles` (lấy `Vehicle_IMD_Decile`).
  * **D2 (Reshaping & time):** Theo dõi xu hướng thay đổi chênh lệch thương vong giữa nhóm khó khăn nhất và khá giả nhất qua từng năm (2011–2015).
  * **D3 (Derived variables):** Tạo biến $\text{Casualties\_per\_Accident}$, tỷ lệ nạn nhân là trẻ em ($\text{Under\_16\_Share}$) và gom nhóm 3 tầng kinh tế (*Most Deprived 1–3*, *Middle 4–7*, *Least Deprived 8–10*).
  * **D4 (Controlling for a confounder):** Kiểm soát `Urban_or_Rural_Area` (do khu vực thu nhập thấp thường tập trung ở các đô thị mật độ dân cư cao).
  * **D5 (Quantifying uncertainty):** Chạy kiểm định phi tham số Kruskal-Wallis / Mann-Whitney U và tính chỉ số độ lớn tác động (Rank-biserial correlation) giữa hai nhóm đầu và cuối thang đo IMD.

---

## Phần 2: Câu hỏi Machine Learning (`03_ml_question.ipynb`)

### Đề bài câu hỏi ML
> Khi nhận được cuộc gọi báo tai nạn giao thông tại hiện trường (trước khi lực lượng y tế tiếp cận nạn nhân), liệu mô hình học máy có thể dự đoán chính xác vụ tai nạn đó thuộc nhóm Nghiêm trọng/Tử vong ($\text{KSI} = \text{Fatal}$ hoặc $\text{Serious}$) hay Nhẹ ($\text{Slight}$) dựa trên thông tin bối cảnh tuyến đường, thời gian, thời tiết và loại phương tiện tham gia hay không — và yếu tố bối cảnh nào đóng vai trò quyết định nhất để ưu tiên điều phối xe cấp cứu?

### Lộ trình triển khai đáp ứng 6/6 yêu cầu bắt buộc

1. **Định nghĩa bài toán, người dùng & chống rò rỉ dữ liệu (Anti-Data Leakage):**
   * **Người dùng mục tiêu:** Trung tâm điều phối khẩn cấp (999 Ambulance Dispatch) cần phân loại mức độ ưu tiên điều xe cứu thương ngay tại thời điểm nhận cuộc gọi báo tin.
   * **Biến mục tiêu ($y$):** Phân loại nhị phân `is_KSI` ($1$ nếu `Accident_Severity` thuộc nhóm `1 - Fatal` hoặc `2 - Serious`; $0$ nếu là `3 - Slight`).
   * **Đặc trưng đầu vào ($X$ — chỉ dùng thông tin có sẵn lúc nhận tin báo):** Thời gian (`Hour`, `Day_of_Week`, `Month`), vị trí & hạ tầng (`Latitude`, `Longitude`, `Road_Type`, `Speed_limit`, `Junction_Detail`, `Junction_Control`, `Urban_or_Rural_Area`), môi trường (`Light_Conditions`, `Weather_Conditions`, `Road_Surface_Conditions`), thông tin sơ bộ hiện trường (`Number_of_Vehicles`, cờ `has_motorcycle` và `has_pedestrian` tổng hợp từ bảng `Vehicles`/`Casualties`).
   * **Danh sách cột loại bỏ để chống Data Leakage (bắt buộc liệt kê rõ trong notebook):**
     * `Accident_Severity`: Biến nhãn gốc.
     * `Number_of_Casualties` và toàn bộ các cột chi tiết thương tích trong bảng `Casualties`: Chỉ xác định được sau khi nhân viên y tế tiếp cận và kiểm tra nạn nhân.
     * `Did_Police_Officer_Attend_Scene_of_Accident`: Thông tin hậu kiểm sau khi cảnh sát xử lý xong hiện trường.
     * `Accident_Index`: Mã định danh duy nhất, không mang giá trị dự báo.

2. **Chiến lược chia tập dữ liệu theo thời gian (Time-based Split):**
   * Do dữ liệu là chuỗi thời gian giai đoạn 2005–2015, không dùng chia ngẫu nhiên (`train_test_split` mặc định) để tránh rò rỉ quy luật tương lai vào quá khứ.
   * **Cách chia chuẩn:** Lấy dữ liệu **2005–2013** ($\approx 82\%$) làm tập huấn luyện (`Train`) và giữ nguyên dữ liệu **2014–2015** ($\approx 18\%$) làm tập kiểm thử (`Test`) nhằm mô phỏng đúng kịch bản triển khai thực tế cho các năm tiếp theo.

3. **So sánh Trivial Baseline + ít nhất 2 mô hình trong `scikit-learn Pipeline`:**
   * **Trivial Baseline:** `DummyClassifier(strategy="most_frequent")` (luôn dự đoán lớp đa số `Slight`).
   * **Mô hình 1 (Tuyến tính diễn giải):** `LogisticRegression(class_weight="balanced", max_iter=1000)`.
   * **Mô hình 2 (Phi tuyến dữ liệu bảng):** `HistGradientBoostingClassifier(class_weight="balanced")` hoặc `RandomForestClassifier` / `LightGBM`.
   * **Pipeline:** Đóng gói toàn bộ bước điền giá trị thiếu (`SimpleImputer`), mã hóa biến phân loại (`OneHotEncoder` / `OrdinalEncoder`) và chuẩn hóa biến số (`StandardScaler`) vào `ColumnTransformer` + `Pipeline` của `scikit-learn` để ngăn rò rỉ dữ liệu giữa các tập validation.

4. **Tinh chỉnh bằng Cross-Validation trên Train, đánh giá Test 1 lần & giải thích Metric:**
   * **Lý do loại bỏ Accuracy:** Dữ liệu mất cân bằng lớp nghiêm trọng ($\approx 15\%$ `KSI` so với $\approx 85\%$ `Slight`). Một mô hình vô dụng luôn đoán `Slight` vẫn đạt $\approx 85\%$ Accuracy nhưng bỏ sót $100\%$ ca nguy kịch cần cấp cứu.
   * **Metric lựa chọn:** Dùng **PR-AUC (`average_precision`)** làm thước đo chính để tối ưu khả năng phát hiện lớp thiểu số `KSI`, kết hợp báo cáo **Recall** (độ nhạy bắt ca nguy kịch) và **F1-score** tại ngưỡng quyết định tối ưu.
   * **Quy trình:** Sử dụng `TimeSeriesSplit` (hoặc `StratifiedKFold`) trên **riêng tập Train 2005–2013** để tinh chỉnh siêu tham số, sau đó đánh giá **đúng 1 lần duy nhất** trên tập Test 2014–2015.

5. **Phân tích lỗi chi tiết (Error Analysis):**
   * Tách riêng nhóm **False Negatives** (ca thực tế tử vong/nặng nhưng mô hình đoán nhẹ — lỗi nguy hiểm nhất trong cấp cứu) và **False Positives** (đoán nhầm ca nhẹ thành nặng).
   * Thống kê tỷ lệ sai số theo từng phân nhóm (`Speed_limit`, `Urban_or_Rural_Area`, `has_pedestrian`) và trích xuất $3–5$ bản ghi cụ thể bị dự đoán sai để phân tích nguyên nhân (ví dụ: va chạm ở tốc độ thấp $30\text{ mph}$ trong nội đô nhưng nạn nhân là người đi bộ cao tuổi hoặc xe hai bánh không có khung bảo vệ).

6. **Diễn giải mô hình & Trả lời câu hỏi ban đầu:**
   * Chạy `permutation_importance` trên tập Test (đối chiếu thêm hệ số trọng số từ `LogisticRegression`) để xác định các đặc trưng tác động mạnh nhất (như `has_motorcycle`, `has_pedestrian`, `Speed_limit`, `Urban_or_Rural_Area`, `Light_Conditions`).
   * Kết luận trả lời trực tiếp câu hỏi nghiên cứu: Mô hình cải thiện đáng kể khả năng sàng lọc ca nguy kịch so với baseline để hỗ trợ điều phối nhanh xe cấp cứu, nhưng tại khu vực nội đô giới hạn $30\text{ mph}$ vẫn cần kết hợp quy tắc ưu tiên bắt buộc nếu cuộc gọi báo có liên quan đến người đi bộ hoặc xe hai bánh.

---

## Gợi ý tổ chức mã nguồn dùng chung (`src/`)

Để tránh lặp lại code giữa 5 notebook phân tích (`02_q01` đến `02_q06`), nhóm nên xây dựng một module dùng chung trong thư mục `src/` (ví dụ `src/utils.py`) đảm nhiệm:
1. Đọc các bảng đã làm sạch từ `data/processed/` với đúng kiểu dữ liệu (`dtype`).
2. Ánh xạ tự động nhãn giải mã từ thư mục `data/contextCSVs/` và chuyển các giá trị `-1` về `NaN`.
3. Cung cấp hàm tính chuẩn các chỉ số dẫn xuất dùng chung ($\text{KSI\_Rate}$, $\text{Vehicles\_per\_Accident}$, $\text{Casualties\_per\_Vehicle}$) và hàm tính khoảng tin cậy Bootstrap CI.