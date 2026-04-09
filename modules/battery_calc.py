import json

class BatteryCalculator:
    def __init__(self, specs_data=None):
        self.specs = specs_data
        # Cấu hình Ops (Giá xăng, điện, lãi suất tiết kiệm)
        self.GAS_PRICE_PER_LITER = 23500 
        self.SAVING_INTEREST_RATE = 0.05 
        self.ELECTRICITY_PRICE_KWH = 3200 
        
        # BỘ DỮ LIỆU ĐẦY ĐỦ (FULL DATA)
        self.market_prices = {
            "O_TO_DIEN": {
                "VF 3": {"buy": 30000000, "rent": 900000, "limit": 0, "consumption_gas": 6, "gas_segment": "Mini SUV (Xăng)", "features": "Màn hình 10 inch, Lazang 16 inch"},
                "VF 5 Plus": {"buy": 80000000, "rent_low": 1600000, "rent_high": 2700000, "limit": 3000, "consumption_gas": 7, "gas_segment": "A-SUV (Xăng)", "features": "6 túi khí, Cảnh báo điểm mù"},
                "VF e34": {"buy": 120000000, "rent_low": 2100000, "rent_high": 3500000, "limit": 3000, "consumption_gas": 8, "gas_segment": "C-SUV (Xăng)", "features": "Cốp điện, Điều khiển giọng nói"},
                "VF 6 Plus": {"buy": 135000000, "rent_low": 2500000, "rent_high": 4200000, "limit": 3000, "consumption_gas": 8.5, "gas_segment": "B-SUV (Xăng)", "features": "ADAS Level 2, Cửa sổ trời"},
                "VF 7 Plus (AWD)": {"buy": 149000000, "rent_low": 2900000, "rent_high": 4800000, "limit": 3000, "consumption_gas": 9, "gas_segment": "SUV Hạng C (Xăng)", "features": "Thiết kế phi thuyền, AWD 260kW"},
                "VF 8 Lux": {"buy": 210000000, "rent_low": 3500000, "rent_high": 5500000, "limit": 3000, "consumption_gas": 10, "gas_segment": "D-SUV (Luxury)", "features": "Gói công nghệ Lux AI, Đỗ xe tự động"},
                "VF 9 Plus": {"buy": 500000000, "rent_low": 4500000, "rent_high": 6900000, "limit": 3000, "consumption_gas": 11, "gas_segment": "E-SUV (Luxury)", "features": "Ghế cơ trưởng, Massage toàn bộ"},
                "VF Wild": {"buy": 250000000, "rent": 4000000, "limit": 0, "consumption_gas": 12, "gas_segment": "Bán tải (Xăng/Dầu)", "features": "Kính panorama, Cửa thông thun xe"}
            },
            "XE_MAY_DIEN": {
                "Evo200 Lite": {"buy": 19900000, "rent": 350000, "consumption_gas": 2.2, "gas_segment": "Xe 50cc", "features": "Quãng đường 205km, Pin LFP"},
                "Feliz S": {"buy": 20000000, "rent": 350000, "consumption_gas": 2.5, "gas_segment": "Xe tay ga phổ thông", "features": "Cốp 25L, Phanh đĩa"},
                "Klara S (2026)": {"buy": 35000000, "rent": 400000, "consumption_gas": 2.5, "gas_segment": "Xe tay ga trung cấp", "features": "Thiết kế Italy, Kết nối eSIM"},
                "Vento S": {"buy": 50000000, "rent": 500000, "consumption_gas": 3.0, "gas_segment": "Xe tay ga cao cấp", "features": "ABS 1 kênh, Side Motor 5200W"},
                "Theon S": {"buy": 70000000, "rent": 600000, "consumption_gas": 3.2, "gas_segment": "Xe tay ga hạng sang", "features": "ABS 2 kênh Continental, Smartkey"}
            }
        }

    def calculate_roi_pro(self, model_name, km_per_month):
        # 1. Kiểm tra đầu vào
        if km_per_month <= 0:
            return {"error": "Số km phải lớn hơn 0 nhé! 😉"}
        
        warning = "Mức di chuyển cực cao! Chú ý bảo trì lốp và phanh thường xuyên." if km_per_month > 10000 else None

        # 2. Tìm Model trong Database
        category = None
        price_info = None
        for cat in self.market_prices:
            if model_name in self.market_prices[cat]:
                category = cat
                price_info = self.market_prices[cat][model_name]
                break
        
        if not price_info:
            return {
                "error": f"Dữ liệu xe '{model_name}' chưa có trong hệ thống.",
                "suggestion": "Bạn có thể thử các model như VF 3, VF 7 Plus hoặc Klara S (2026)."
            }

        # 3. Tính phí thuê pin hàng tháng
        if category == "O_TO_DIEN":
            if price_info.get("limit") == 0: 
                monthly_rent_fee = price_info["rent"]
            else: 
                monthly_rent_fee = price_info["rent_low"] if km_per_month <= price_info["limit"] else price_info["rent_high"]
        else: 
            monthly_rent_fee = price_info["rent"]

        # 4. So sánh TCO (Xe Xăng vs Xe Điện)
        ev_cons = 15 if category == "O_TO_DIEN" else 3
        cost_ev = (km_per_month / 100) * ev_cons * self.ELECTRICITY_PRICE_KWH
        cost_gas = (km_per_month / 100) * price_info["consumption_gas"] * self.GAS_PRICE_PER_LITER
        
        monthly_saving = cost_gas - cost_ev - monthly_rent_fee

        # 5. Chi phí cơ hội & Điểm hòa vốn
        buy_price = price_info["buy"]
        opp_cost = (buy_price * self.SAVING_INTEREST_RATE) / 12
        net_saving_per_month = monthly_rent_fee - opp_cost

        if net_saving_per_month <= 0:
            break_even_years = "N/A (Thuê pin hời hơn gửi tiết kiệm)"
        else:
            break_even_years = round((buy_price / net_saving_per_month) / 12, 1)

        # 6. Tạo bảng Markdown hiển thị
        table = f"""
| Hạng mục | Thông số chi tiết |
| :--- | :--- |
| **Dòng xe** | {model_name} ({category.replace('_', ' ')}) |
| **Phân khúc so sánh** | {price_info['gas_segment']} |
| **Phí thuê pin tháng** | {int(monthly_rent_fee):,} VNĐ |
| **Tiết kiệm so với xăng** | {int(max(0, monthly_saving)):,} VNĐ/tháng |
| **Hòa vốn mua đứt** | {break_even_years} năm |
| **Tính năng nổi bật** | {price_info.get('features', 'Đang cập nhật')} |
"""
        return {
            "model": model_name,
            "km": km_per_month,
            "table": table,
            "saving_vs_gas": f"{int(max(0, monthly_saving)):,}",
            "break_even_years": break_even_years,
            "warning": warning,
            "features": price_info.get('features', 'N/A')
        }
