import json
import os
import random

def normalize(text):
    return str(text).lower().strip().replace(" ", "").replace("-", "")

def get_vehicle_reviews(model_name: str = None, specs: list = None, react: str = None):
    # Kiểm tra đầu vào tối thiểu
    if not any([model_name, specs, react]):
        return "Vui lòng nhập tên xe, chủ đề hoặc loại đánh giá để tôi tìm kiếm."

    try:
        data_path = os.path.join('data', 'vinfast_reviews.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        # --- BƯỚC 1: XỬ LÝ ARGUMENTS RỖNG (Lấy toàn bộ nếu rỗng) ---
        # 1. Xử lý xe
        car_list = []
        if model_name:
            target = normalize(model_name)
            car_list = [k for k in all_data.keys() if target in normalize(k)]
        else:
            car_list = list(all_data.keys())

        # 2. Xử lý cảm xúc
        react_list = ["positive", "neutral", "negative"]
        if react and react.lower() in react_list:
            react_list = [react.lower()]

        # 3. Xử lý từ khóa (Normalize specs)
        norm_specs = [normalize(s) for s in specs] if specs else []

        # --- BƯỚC 2: SEARCH CHÍNH THỨC (Tìm phần giao của Car + React + Specs) ---
        def perform_search(cars, reacts, keywords):
            results = {}
            for car in cars:
                car_matches = {}
                for cat in reacts:
                    sentences = all_data[car].get(cat, [])
                    if not keywords:
                        # Nếu không có từ khóa, lấy mẫu 2 câu
                        if sentences: car_matches[cat] = random.sample(sentences, min(len(sentences), 2))
                    else:
                        # Lọc theo keyword
                        matched = [snt for snt in sentences if any(kw in normalize(snt) for kw in keywords)]
                        if matched: car_matches[cat] = matched
                if car_matches:
                    results[car] = car_matches
            return results

        # Thực hiện tìm kiếm lần 1 (Đầy đủ điều kiện)
        final_results = perform_search(car_list, react_list, norm_specs)

        # --- BƯỚC 3: CƠ CHẾ RECOMMEND (Nếu search lần 1 thất bại) ---
        if not final_results:
            status_msg = ""
            
            # Case A: Không tìm thấy Specs -> Bỏ specs, lấy Car + React làm gợi ý
            if norm_specs:
                final_results = perform_search(car_list, react_list, [])
                status_msg = f"Tôi không tìm thấy đánh giá về '{specs}', nhưng đây là các trải nghiệm chung về dòng xe này."
            
            # Case B: Không tìm thấy Car (hoặc Car rỗng) -> Bỏ Car, lấy Specs + React làm gợi ý trên toàn sàn
            elif model_name:
                final_results = perform_search(list(all_data.keys()), react_list, norm_specs)
                status_msg = f"Dòng xe '{model_name}' chưa có đánh giá này, bạn có thể tham khảo các dòng xe khác có cùng đặc điểm '{specs}'."

            if final_results:
                final_results["_status"] = status_msg

        return final_results if final_results else "Không tìm thấy dữ liệu phù hợp."

    except Exception as e:
        return f"Lỗi hệ thống review: {str(e)}"
