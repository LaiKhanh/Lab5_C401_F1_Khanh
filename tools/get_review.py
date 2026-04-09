import json
from tools.review import get_vehicle_reviews

def print_test_result(title, result):
    print(f"\n{'='*30}")
    print(f"TEST: {title}")
    print(f"{'='*30}")
    if isinstance(result, dict):
        # Kiểm tra xem có phải là hàng fallback (gợi ý) không
        if "_status" in result:
            print(f"💡 THÔNG BÁO HỆ THỐNG: {result['_status']}")
        
        # Loại bỏ key _status trước khi in dữ liệu để sạch sẽ
        display_data = {k: v for k, v in result.items() if k != "_status"}
        print(json.dumps(display_data, indent=4, ensure_ascii=False))
    else:
        print(result)

if __name__ == "__main__":
    # --- CASE 1: Khớp hoàn toàn (Giao của 3 điều kiện) ---
    # Tìm review TIÊU CỰC về PHẦN MỀM của VF 8 Lux
    print_test_result(
        "Khớp hoàn toàn 3 tham số",
        get_vehicle_reviews(model_name="VF 8 Lux", specs=["phần mềm"], react="negative")
    )

    # --- CASE 2: Khuyết tham số (Lấy cả data của tham số đó) ---
    # Không có model_name -> Tìm tất cả xe có khen ngợi về "pin LFP"
    print_test_result(
        "Khuyết model_name (Search toàn sàn)",
        get_vehicle_reviews(model_name=None, specs=["LFP"], react="positive")
    )

    # --- CASE 3: Khuyết specs (Lấy review tổng quan) ---
    # Tìm review bất kỳ về Klara S
    print_test_result(
        "Khuyết specs (Lấy review ngẫu nhiên)",
        get_vehicle_reviews(model_name="Klara S", specs=None, react=None)
    )

    # --- CASE 4: RECOMMEND - Không thấy Specs (Hạ cấp lấy Car + React) ---
    # Tìm "sang trọng" trong VF 3 (Chắc chắn không có trong data thô)
    # Kỳ vọng: Trả về review ngẫu nhiên của VF 3 kèm thông báo
    print_test_result(
        "Hạ cấp: Không thấy Specs (Gợi ý xe hiện tại)",
        get_vehicle_reviews(model_name="VF 3", specs=["sang trọng"], react="positive")
    )

    # --- CASE 5: RECOMMEND - Không thấy Model (Hạ cấp lấy Specs trên toàn sàn) ---
    # Tìm "lỗi phanh" của một xe không tồn tại "VF 10"
    # Kỳ vọng: Trả về review lỗi phanh của các xe khác (VF 8, Theon...) kèm thông báo
    print_test_result(
        "Hạ cấp: Không thấy Model (Gợi ý xe khác cùng đặc điểm)",
        get_vehicle_reviews(model_name="VF 10", specs=["phanh"], react="negative")
    )

    # --- CASE 6: Chặn lỗi đầu vào rỗng ---
    print_test_result(
        "Lỗi: Rỗng toàn bộ",
        get_vehicle_reviews(None, None, None)
    )
