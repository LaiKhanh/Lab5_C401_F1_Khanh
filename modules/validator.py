import re

def handle_exception(user_input: str):
    user_input = user_input.strip()

    # 1. Empty
    if not user_input:
        return {
            "status": "error",
            "message": "Bạn hãy nhập nhu cầu mua xe nhé."
        }

    # 2. Too short / meaningless
    if len(user_input) < 2:
        return {
            "status": "error",
            "message": "Bạn có thể mô tả rõ hơn nhu cầu không?"
        }

    # 3. No real language (only symbols/numbers)
    if not re.search(r"[a-zA-Zà-ỹ]", user_input.lower()):
        return {
            "status": "error",
            "message": "Mình chưa hiểu yêu cầu, bạn có thể nhập lại rõ hơn không?"
        }

    # 4. Negative numbers
    numbers = re.findall(r"-?\d+", user_input)
    for num in numbers:
        try:
            if int(num) < 0:
                return {
                    "status": "error",
                    "message": "Giá trị không hợp lệ (không thể là số âm)."
                }
        except:
            pass

    return {
        "status": "ok",
        "cleaned_input": user_input
    }