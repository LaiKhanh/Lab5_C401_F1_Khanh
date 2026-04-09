# SPEC — AI Product Hackathon

**Nhóm:** C401-F1 <br>

**Track:** ☑ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool · ☐ XanhSM · ☐ Open <br>

**Problem statement (1 câu):** *Ai gặp vấn đề gì, hiện giải thế nào, AI giúp được gì*
Khách hàng mua xe VinFast bị nhiễu loạn thông tin. Website hãng thì khô khan (chỉ có thông số), còn hội nhóm thì hỗn loạn (khó kiểm chứng). Khách mất nhiều thời gian tự tổng hợp, gây chậm trễ quyết định mua xe. AI có thể kết hợp dữ liệu kỹ thuật và review thực tế để tư vấn chính xác, đa chiều ngay lập tức.

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | **User:** *khách hàng đang quan tâm mua xe Vinfast nhưng chưa biết chọn loại nào.* <br> **Pain:** *khách hàng bị nhiễu loạn thông tin và mất thời gian (30-40 phút) khi phải tự tổng hợp thông tin từ nhiều nguồn (thông số kĩ thuật trên website, review trên các hội nhóm).* <br> **Value:** *trả lời ngay lập tức, hoạt động 24/7, tổng hợp thông tin từ các nguồn đồng thời phân tích nhu cầu người dùng để đề xuất mẫu xe phù hợp.* | **Khi AI sai:** *user không tìm được mẫu xe phù hợp với nhu cầu, hiểu sai hoặc nhầm lẫn về thông tin xe.* <br> **User biết AI sai:** *check lại thông tin mẫu xe trên website hoặc từ nhân viên bán hàng.* <br> **User sửa:** *yêu cầu đề xuất lại, chỉnh lại thông tin đầu vào, chuyển sang nhân viên tư vấn thật nếu cần.* | **Cost:** *~$0.01-$0.02/request <br> **Latency:** *1-3 giây/response* <br> **Risk chính:** *AI hallucinate thông tin xe, người dùng tin AI quá mức không check lại thông tin mẫu xe được đề xuất.* |

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation <br>
Justify: *Augmentation — AI tư vấn và đề xuất mẫu xe nhưng quyết định mua xe vẫn do khách hàng.*

**Learning signal:**

1. User correction đi vào đâu?
*-> User correction trở thành context bổ sung cho AI để cải thiện recommendation.*
2. Product thu signal gì để biết tốt lên hay tệ đi?
*-> User click vào mẫu xe AI gợi ý.*
3. Data thuộc loại nào? ☑ User-specific · ☑ Domain-specific · ☐ Real-time · ☑ Human-judgment · ☐ Khác:
4. Có marginal value không? (Model đã biết cái này chưa?)
*-> Có. Data này được thu thập trực tiếp từ người dùng khi chọn xe giúp model học từ sai sót và cá nhân hóa trải nghiệm người dùng từ đó cải thiện AI recommendation.*
---

## 2. User Stories — 4 paths

Mỗi feature chính = 1 bảng. AI trả lời xong → chuyện gì xảy ra?

### Feature 1: *AI Tư vấn Đa chiều (Specs + Real-world Reviews)*

**Trigger:** *Khách hàng hỏi về một thông số cụ thể (VD: "Pin VF 8 chạy thực tế hỗn hợp được bao xa?") → AI truy xuất thông số kỹ thuật của hãng + phân tích hàng ngàn review từ các chủ xe xác thực → Đưa ra câu trả lời kết hợp cả 2 góc nhìn.*

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | *AI trả lời: "Theo NSX, dải hoạt động là 400km. Tuy nhiên, tổng hợp từ 500+ review thực tế từ chủ xe trên các diễn đàn, mức pin thực tế thường đạt 320-350km khi bật full điều hòa." Kèm theo là biểu đồ tỉ lệ hài lòng. User thấy chân thực, tin tưởng và chuyển sang bước hỏi giá lăn bánh.* |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | *Khách hỏi về một bản cập nhật phần mềm mới ra mắt hôm qua. AI báo: "Phần mềm này vừa phát hành. Thông số hãng cập nhật là [X], nhưng AI chưa thu thập đủ dữ liệu review thực tế để đánh giá khách quan. Bạn có muốn xem review của phiên bản ngay trước đó không?" → User quyết định xem bản cũ hoặc chờ thêm.* |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | *AI trích xuất nhầm review của VF 9 để tư vấn cho VF 8 (VD: "VF 8 có ghế massage hàng 2 rất êm..."). User đọc và nhận ra ngay thông tin vô lý vì VF 8 không có tính năng này. Dưới câu trả lời có nút "Báo cáo thông tin sai lệch".* |
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | *User bấm "Báo cáo", chọn lý do "Trích dẫn sai dòng xe". AI ngay lập tức xin lỗi và gỡ bỏ đoạn review đó khỏi màn hình. Log data (ID câu trả lời + Tag lỗi) được gửi về pipeline Retraining để tinh chỉnh lại thuật toán Phân loại dữ liệu (Review Classifier).* |


### Feature 2: *AI Kiểm chứng Tin đồn (Fact-Checker / Myth Buster)*

**Trigger:** *Khách hàng copy/paste một bình luận gây hoang mang từ Facebook (VD: "Thấy bảo lô VF 6 mới hay bị lỗi đen màn hình?") → AI quét chéo nội dung này với lịch sử bảo hành chính thức và sentiment analysis (phân tích cảm xúc) của cộng đồng trong 3 tháng gần nhất → Đưa ra kết luận xác thực.*

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | *AI hiển thị thẻ [ĐÃ KIỂM CHỨNG] và trả lời: "Đây là lỗi từ lô hàng đầu năm 2023. VinFast đã ra bản cập nhật phần mềm 8.x khắc phục triệt để. Dữ liệu 3 tháng qua cho thấy 98% chủ xe không còn gặp tình trạng này." User giải tỏa được tâm lý hoang mang và tự tin chốt cọc.* |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | *Sự cố khách hỏi miêu tả quá mơ hồ hoặc rải rác. AI báo: "Hệ thống ghi nhận có một số ít thảo luận về vấn đề này, nhưng chưa có kết luận kỹ thuật chính thức. Bạn có muốn tôi kết nối bạn trực tiếp với Chuyên viên Kỹ thuật để hỏi rõ hơn không?"* |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | *AI khẳng định 100% "Đây là tin giả, xe không bị lỗi này" (thiên lệch bảo vệ hãng), nhưng bản thân user lại đang có bạn bè bị lỗi đó thật. User cảm thấy AI lấp liếm và mất niềm tin.* |
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | *User bấm "Không hữu ích (Thumbs down)" và nhập phản hồi: "Tôi biết người đi xe này vẫn bị". Dữ liệu này không chỉ dùng để train AI bớt tính "thiên vị" (bias), mà còn được đẩy thẳng vào một Dashboard Cảnh báo (Escalation) cho đội ngũ Chăm sóc khách hàng và Kỹ thuật của VinFast để hãng nắm bắt vấn đề thực tế.* |
---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** ☑ Precision · ☐ Recall <br>

**Tại sao?** <br> *Sai thông tin (giá xe, chính sách pin, thông số kỹ thuật) gây mất niềm tin lớn và có thể ảnh hưởng đến quyết định mua xe. Automotive là high-consideration → độ chính xác quan trọng hơn độ đầy đủ.*

**Nếu sai ngược lại thì chuyện gì xảy ra?** <br> 
*Nếu recall thấp → có thể fallback sang human hoặc nguồn chính thức. Nhưng nếu precision thấp → user tin thông tin sai → rủi ro lớn (mất trust, mất deal, thậm chí legal/PR risk).*

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| *Answer Accuracy (Factual Correctness)* | *≥90% (ideal ≥95%)* | *<85%* |
| *Task Success Rate (% session đạt goal)* | *≥60% (ideal ≥80%)* | *<50%* |
| *Hallucination Rate* | *≤1%* | *>5%* |
---

## 4. Top 3 failure modes

*Liệt kê cách product có thể fail — không phải list features.*
*"Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."*

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 | *Chatbot VinFast: dữ liệu xe (giá, phiên bản, thông số) bị outdated hoặc retrieval lấy nhầm nguồn cũ* | *AI trả lời tự tin nhưng sai → user không biết bị sai, tin thông tin và ra quyết định mua sai* | *Kết nối nguồn dữ liệu real-time (API) hoặc data được crawl thường xuyên, hiển thị timestamp, thêm bước kiểm tra độ tin cậy → nếu thấp thì không trả lời dứt khoát* |
| 2 | *Chatbot tư vấn mua xe: user hỏi câu phức tạp hoặc ngoài scope (so sánh, nhu cầu đặc thù)* | *Bot trả lời không nhất quán / dừng giữa chừng → user không hiểu là hệ thống fail hay không hỗ trợ* | *Detect intent rõ ràng, nếu không chắc → hỏi lại để làm rõ; luôn trả về response có ích thay vì im lặng* |
| 3 | *Chatbot cung cấp thông tin quy trình (đặt cọc, giao xe, bảo hành): policy thay đổi theo thời gian hoặc theo khu vực* | *AI đưa hướng dẫn không chính xác → user làm theo nhưng chỉ phát hiện sai khi đã thực hiện (ví dụ: đặt cọc sai cách, hiểu sai điều kiện bảo hành)* | *Gắn rõ “policy có thể thay đổi”, link trực tiếp nguồn chính thức, và với thông tin quan trọng → bắt buộc xác nhận lại hoặc chuyển human* |
---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | *200 lượt hỏi/ngày, 20% khách để lại thông tin (lead)* | *1,000 lượt hỏi/ngày, 35% khách để lại thông tin* | *5,000 lượt hỏi/ngày, 50% khách để lại thông tin* |
| **Cost** | *$30/ngày (API cơ bản, ít vector data)* | *$150/ngày (Data cập nhật thường xuyên, infra ổn định)* | *$600/ngày (Fine-tuning, RAG thời gian thực, infra tải cao)* |
| **Benefit** | *Tiết kiệm 2 tư vấn viên trực chat $\rightarrow$ 16 giờ/ngày* | *Tiết kiệm 10 tư vấn viên $\rightarrow$ 80 giờ/ngày + Tăng tỷ lệ chốt đơn nhờ review khách quan* | *Thay thế đội ngũ trực chat quy mô lớn $\rightarrow$ 400 giờ/ngày + Lead chất lượng cao từ dữ liệu review* |
| **Net** | *Tiết kiệm ~$400/ngày - $30 = +$370/ngày* | *+$2,000/ngày - $150 = +$1,850/ngày* | *+$10,000/ngày - $600 = +$9,400/ngày* |

**Kill criteria: Dự án sẽ bị hủy bỏ nếu** <br>
**Acceptance rate < 40% sau 1 tháng:** *Khách hàng đánh giá câu trả lời của chatbot không hữu ích hoặc thông tin review bị sai lệch quá nhiều.* <br>
**Cost > Benefit 2 tháng liên tục:** *Chi phí API để xử lý lượng lớn dữ liệu review vượt quá giá trị mà lượng lead mang lại.* <br>
**Hallucination Rate > 5%:** *AI tự bịa ra các lỗi của xe hoặc thông số không có trong review gây ảnh hưởng đến uy tín thương hiệu.*

---

## 6. Mini AI spec (1 trang)

*Tóm tắt tự do — viết bằng ngôn ngữ tự nhiên, không format bắt buộc.*
*Gom lại: product giải gì, cho ai, AI làm gì (auto/aug), quality thế nào (precision/recall), risk chính, data flywheel ra sao.*
