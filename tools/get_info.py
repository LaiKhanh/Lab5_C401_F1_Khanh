import json
import os

def normalize(text):
    return str(text).lower().strip().replace(" ", "").replace("-", "")

def get_vehicle_info(model_name: str = None, specs: list = None):
    """
    Tìm kiếm thông tin xe dựa trên tên model hoặc thông số kỹ thuật:
    - Nếu có model_name: Tìm xe đó (chấp nhận viết tắt/thiếu). Lọc specs nếu có.
    - Nếu model_name trống: Tìm tất cả xe có thông số khớp với specs.
    """
    try:
        # 1. Load Data
        data_path = os.path.join('data', 'vinfast_specs.json')
        if not os.path.exists(data_path):
            return "Lỗi: Không tìm thấy file vinfast_specs.json tại thư mục data/"
            
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. Flatten Data (Phẳng hóa để search nhanh)
        all_vehicles = {}
        for cat in data:
            for name, details in data[cat].items():
                all_vehicles[name] = details

        # --- KỊCH BẢN 1: CÓ TÊN XE (Tìm chính xác hoặc gần đúng) ---
        if model_name and model_name.strip():
            target_name = normalize(model_name)
            found_car_key = None
            
            # Ưu tiên 1: Khớp hoàn toàn (sau khi normalize)
            for full_name in all_vehicles:
                if target_name == normalize(full_name):
                    found_car_key = full_name
                    break
            
            # Ưu tiên 2: Khớp một phần (Xử lý vụ nhập "VF 5" tìm ra "VF 5 Plus")
            if not found_car_key:
                for full_name in all_vehicles:
                    if target_name in normalize(full_name):
                        found_car_key = full_name
                        break
            
            if found_car_key:
                car_details = all_vehicles[found_car_key]
                if not specs: 
                    return {found_car_key: car_details}
                
                # Lọc specs cụ thể cho xe đã tìm thấy
                filtered_info = {}
                for spec in specs:
                    spec_norm = normalize(spec)
                    # Tìm ở level 1 và level 2 (nested dict)
                    for key, value in car_details.items():
                        if spec_norm in normalize(key):
                            filtered_info[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if spec_norm in normalize(sub_key):
                                    filtered_info[sub_key] = sub_value
                
                return {found_car_key: filtered_info} if filtered_info else {found_car_key: car_details}
            
            return f"Không tìm thấy dòng xe nào khớp với từ khóa '{model_name}'."

        # --- KỊCH BẢN 2: CHỈ CÓ SPECS (Tìm tất cả xe có thông số này) ---
        elif specs:
            global_matches = {}
            for full_name, details in all_vehicles.items():
                matched_data = {}
                for spec in specs:
                    spec_norm = normalize(spec)
                    for key, value in details.items():
                        if spec_norm in normalize(key):
                            matched_data[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if spec_norm in normalize(sub_key):
                                    matched_data[sub_key] = sub_value
                
                if matched_data:
                    global_matches[full_name] = matched_data
            
            return global_matches if global_matches else "Không tìm thấy thông số yêu cầu trên toàn hệ thống."

        return "Vui lòng nhập tên xe hoặc thông số bạn quan tâm."

    except Exception as e:
        return f"Lỗi hệ thống trong info.py: {str(e)}"
