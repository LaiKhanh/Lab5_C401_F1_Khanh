# SPEC draft — Nhóm C401-F1

## Track: VinFast

## Problem statement

Khách hàng mua xe VinFast bị nhiễu loạn thông tin. Website hãng thì khô khan (chỉ có thông số), còn hội nhóm thì hỗn loạn (khó kiểm chứng). Khách mất nhiều thời gian tự tổng hợp, gây chậm trễ quyết định mua xe. AI có thể kết hợp dữ liệu kỹ thuật và review thực tế để tư vấn chính xác, đa chiều ngay lập tức.

## Canvas draft

| Value                                                                                                                                                                                                                                                                                                                                                                                                                                 | Trust                                                                                                                                                                                                                                                                                                                      | Feasibility                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **User:** khách hàng đang quan tâm mua xe Vinfast nhưng chưa biết chọn loại nào.<br><br>**Pain:** khách hàng bị nhiễu loạn thông tin và mất thời gian (30–40 phút) khi phải tự tổng hợp thông tin từ nhiều nguồn (thông số kĩ thuật trên website, review trên các hội nhóm).<br><br>**Value:** trả lời ngay lập tức, hoạt động 24/7, tổng hợp thông tin từ các nguồn đồng thời phân tích nhu cầu người dùng để đề xuất mẫu xe phù hợp | **Khi AI sai:** user không tìm được mẫu xe phù hợp với nhu cầu, hiểu sai hoặc nhầm lẫn về thông tin xe.<br><br>**User biết AI sai:** check lại thông tin mẫu xe trên website hoặc từ nhân viên bán hàng.<br><br>**User sửa:** yêu cầu đề xuất lại, chỉnh lại thông tin đầu vào, chuyển sang nhân viên tư vấn thật nếu cần. | **Cost:** $0.01–$0.02/request<br><br>**Latency:** 1–3 giây/response<br><br>**Risk chính:** AI hallucinate thông tin xe, người dùng tin AI quá mức không check lại thông tin mẫu xe được đề xuất. |

**Auto hay aug?** Augmentation — AI tư vấn và đề xuất mẫu xe nhưng quyết định mua xe vẫn do khách hàng.

**Learning signal:** <br>
User correction đi vào đâu? -> User correction trở thành context bổ sung cho AI để cải thiện recommendation.<br>

Product thu signal gì để biết tốt lên hay tệ đi? -> User click vào mẫu xe AI gợi ý.<br>

Data thuộc loại nào? -> Domain-specific, Human-judgement, User-specific.<br>

Có marginal value không? -> Có. Data này được thu thập trực tiếp từ người dùng khi chọn xe giúp model học từ sai sót và cá nhân hóa trải nghiệm người dùng từ đó cải thiện AI recommendation.

## Hướng đi chính

- Prototype: chatbot đơn giản hỏi về 1 sản phẩm cụ thể → đưa ra thông số + review thực tế
- Eval: Độ chính xác thông số (100%), độ tự nhiên của câu trả lời (>80%).
- Main failure mode: dữ liệu xe (giá, phiên bản, thông số) bị outdated hoặc retrieval lấy nhầm nguồn cũ -> AI trả lời tự tin nhưng sai → user không biết bị sai, tin thông tin và ra quyết định mua sai

## Phân công

- Lại Gia Khánh: Canvas
- Lê Duy Anh: User stories 4 paths
- Trương Minh Sơn: Eval metrics
- Bùi Trần Gia Bảo: Failure mode
- Nguyễn Phạm Trà My: ROI 3 kịch bản
- Mạc Phương Nga: Mini AI spec
