from modules.validator import handle_exception
from modules.llm_handler import llm_agent

def main():
    print("="*60)
    print("VINFAST AI CONSULTANT - CHẾ ĐỘ TERMINAL (CLI TEST)")
    print("="*60)
    print("Gõ 'q', 'quit', hoặc 'exit' để thoát.\n")
    
    # Ở chế độ Terminal, ta cấp 1 session_id cứng để Agent nhớ được mạch hội thoại
    session_id = "test_user_session"
    
    while True:
        try:
            user_input = input("\nBạn: ")
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("\nKết thúc phiên thử nghiệm. Tạm biệt!")
                break
            
            if not user_input.strip():
                continue
                
            print("\nAI đang suy nghĩ (và gọi tool nếu cần)...")
            validation = handle_exception(user_input)

            if validation["status"] != "ok":
                print(f"\nAI: {validation['message']}")
                print("-" * 60)
                continue

            clean_input = validation["cleaned_input"]

            response = llm_agent.get_response(clean_input, session_id=session_id)
            
            if response["status"] != "ok":
                print(f"\nAI: {response['message']}")
            else:
                print(f"\nAI: {response['content']}")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nKết thúc phiên thử nghiệm. Tạm biệt!")
            break
        except Exception as e:
            print(f"\n[Lỗi hệ thống]: {e}")

if __name__ == "__main__":
    main()
