## Canvas

|              | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Trust                                                                                                                                                                                                                                                                                                                                                                           | Feasibility                                                                                                                                                                                                                                          |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chi tiết** | **User:** Khách hàng đang có nhu cầu mua vé (đi du lịch, công tác, thăm thân).<br>**Pain:** Ngại vào web/app thao tác qua nhiều màn hình phức tạp (chọn ngày, điểm đi/đến, lọc giá). Cần một công cụ hỏi-đáp nhanh gọn để "chốt" lịch.<br>**Auto hay Aug:** Auto (Bot tự động trích xuất thông tin từ câu chat và trả về danh sách chuyến bay trực tiếp).<br>**Value:** Tiết kiệm thời gian, trải nghiệm mượt mà, giúp VNA rút ngắn phễu bán hàng (từ lúc có nhu cầu đến lúc click mua). | **Precision cao:** Đây là yếu tố sống còn. Sai ngày, sai điểm đến, hoặc sai giá vé sẽ làm mất lòng tin ngay lập tức.<br>**Khi sai:** User nhận ra lỗi ngay khi thấy kết quả không đúng. Giải pháp: thêm nút "Đổi ngày bay", "Đổi điểm đến".<br>**Recovery:** "Xin lỗi, có vẻ NEO bắt nhầm thông tin. Để chính xác nhất, bạn vui lòng chọn điểm khởi hành từ danh sách sau nhé." | **Cost:** Chi phí LLM/NLP + băng thông tra cứu vé.<br>**Latency:** Phải < 3 giây, nếu chậm user sẽ rời đi.<br>**Risk:** Giá vé thay đổi real-time → lệch giá giữa bot và thanh toán.<br>**Dep:** Phụ thuộc API hệ thống đặt giữ chỗ (Sabre/Amadeus). |

---

## Automation hay augmentation?

☐ Automation — AI làm thay, user không can thiệp  
☑ Augmentation — AI gợi ý, user quyết định cuối cùng

**Justify:** Việc phân loại giao dịch sai có thể ảnh hưởng lớn đến việc quản lý chi tiêu của user. Vì user được phép chỉnh sửa phân loại, user cần có quyền quyết định cuối cùng để đảm bảo tính chính xác, do đó đây là mô hình Augmentation.

---

## Learning signal

| #   | Câu hỏi                                          | Trả lời                                                                                                                                             |
| --- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | User correction đi vào đâu?                      | Dữ liệu correction của user (phân loại chính xác) được dùng để huấn luyện lại mô hình (retraining).                                                 |
| 2   | Product thu signal gì để biết tốt lên hay tệ đi? | Tỷ lệ user chấp nhận (acceptance rate) hoặc sửa (correction rate) gợi ý của AI. Các chỉ số về độ chính xác (Precision/Recall) của mô hình hiện tại. |
| 3   | Data thuộc loại nào?                             | ☑ User-specific · ☐ Domain-specific · ☑ Real-time · ☑ Human-judgment · ☐ Khác: \_\_\_                                                               |

**Có marginal value không?** (Model đã biết cái này chưa? Ai khác cũng thu được data này không?):<br>
Có. Data correction của từng user là User-specific và Human-judgment. Đây là dữ liệu nhãn vàng có giá trị cao, giúp model học hỏi từ sai sót và cá nhân hóa trải nghiệm cho người dùng, điều mà các model chung (Domain-specific) sẽ không có được.
