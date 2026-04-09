import json

class BatteryCalculator:
    def __init__(self, specs_data):
        self.specs = specs_data
        # Cấu hình giá xăng và lãi suất tiết kiệm (Các thông số Ops)
        self.GAS_PRICE_PER_LITER = 23500  # VNĐ
        self.SAVING_INTEREST_RATE = 0.05  # 5%/năm cho chi phí cơ hội
        self.ELECTRICITY_PRICE_KWH = 3200 # Giá điện trung bình sạc tại trụ
        
        # Bảng giá Pin & Thuê 
        self.market_prices = {
            "O_TO_DIEN": {
                "VF 3": {"buy": 30000000, "rent": 900000, "limit": 0, "gas_segment": "Hạng A (6L/100km)", "consumption_gas": 6},
                "VF 5 Plus": {"buy": 80000000, "rent_low": 1600000, "rent_high": 2700000, "limit": 3000, "gas_segment": "Hạng A/B (7L/100km)", "consumption_gas": 7},
                "VF 7 Plus (AWD)": {"buy": 149000000, "rent_low": 2900000, "rent_high": 4800000, "limit": 3000, "gas_segment": "SUV Hạng C (9L/100km)", "consumption_gas": 9},
                "VF 9 Plus": {"buy": 500000000, "rent_low": 4500000, "rent_high": 6900000, "limit": 3000, "gas_segment": "SUV Hạng E (11L/100km)", "consumption_gas": 11}
            },
            "XE_MAY_DIEN": {
                "DEFAULT": {"buy": 19900000, "rent": 350000, "gas_segment": "Xe tay ga (2.5L/100km)", "consumption_gas": 2.5}
            }
        }

    def calculate_roi_pro(self, model_name, km_per_month):
        # --- BƯỚC 1: XỬ LÝ DỮ LIỆU ĐỘNG (EDGE CASES) ---
        if km_per_month <= 0:
            return {"error": "Số km phải lớn hơn 0 nhé! Bạn định cất xe trong kho à? 😉"}
        

        
        if km_per_month > 10000:
            warning = "Mức di chuyển cực cao! Bạn nên chú ý lịch bảo dưỡng lốp và hệ thống phanh dày hơn thông thường."
        else:
            warning = None

        # Tìm model và xử lý gợi ý xe tương đương
        category = None
        price_info = None
        
        for cat in ["O_TO_DIEN", "XE_MAY_DIEN"]:
            if model_name in self.market_prices[cat]:
                category = cat
                price_info = self.market_prices[cat][model_name]
                break
        
        if not price_info:
            # Gợi ý xe tương đương nếu không có trong data
            return {
                "error": f"Dữ liệu xe '{model_name}' đang được cập nhật.",
                "suggestion": "Bạn có thể tham khảo 'VF 7 Plus (AWD)' nếu thích xe gầm cao hoặc 'VF 5 Plus' cho xe đô thị."
            }

        # --- BƯỚC 2: TÍNH TOÁN LOGIC THUÊ PIN ---
        if category == "O_TO_DIEN":
            if price_info.get("limit") == 0:
                monthly_rent_fee = price_info["rent"]
            else:
                monthly_rent_fee = price_info["rent_low"] if km_per_month <= price_info["limit"] else price_info["rent_high"]
        else:
            monthly_rent_fee = self.market_prices["XE_MAY_DIEN"]["DEFAULT"]["rent"]

        # --- BƯỚC 3: SO SÁNH CHI PHÍ XE XĂNG (TCO) ---
        # Giả định mức tiêu thụ điện trung bình (kWh/100km)
        ev_consumption = 15 if category == "O_TO_DIEN" else 3 # 15kWh/100km cho ô tô, 3kWh cho xe máy
        cost_ev_energy = (km_per_month / 100) * ev_consumption * self.ELECTRICITY_PRICE_KWH
        
        cost_gas_fuel = (km_per_month / 100) * price_info["consumption_gas"] * self.GAS_PRICE_PER_LITER
        monthly_saving_vs_gas = cost_gas_fuel - cost_ev_energy - monthly_rent_fee

        # --- BƯỚC 4: YẾU TỐ THỜI GIAN & CHI PHÍ CƠ HỘI ---
        buy_price = price_info["buy"]
        opportunity_cost_monthly = (buy_price * self.SAVING_INTEREST_RATE) / 12
        
        # Điểm hòa vốn thực tế (có tính đến việc tiền đẻ ra tiền nếu không mua pin)
        # Công thức: Mua pin hòa vốn khi (Giá mua) < (Phí thuê - Lãi tiết kiệm bỏ lỡ) * Số tháng
        net_saving_per_month = monthly_rent_fee - opportunity_cost_monthly
        
        if net_saving_per_month <= 0:
            break_even_years = "Không bao giờ (Gửi tiết kiệm hời hơn)"
        else:
            break_even_months = buy_price / net_saving_per_month
            break_even_years = round(break_even_months / 12, 1)

        return {
            "model": model_name,
            "km": km_per_month,
            "monthly_rent_fee": f"{monthly_rent_fee:,}",
            "saving_vs_gas": f"{max(0, int(monthly_saving_vs_gas)):,}",
            "opportunity_cost_monthly": f"{int(opportunity_cost_monthly):,}",
            "break_even_years": break_even_years,
            "warning": warning,
            "gas_segment": price_info["gas_segment"]
        }