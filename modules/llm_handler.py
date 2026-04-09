import os
import re
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Import list công cụ từ file tools.py
from tools.tools import agent_tools

class VinFastLLMHandler:
    def __init__(self):
        load_dotenv()
        if not os.environ.get("OPENAI_API_KEY"):
            print("CẢNH BÁO: Chưa có OPENAI_API_KEY trong file .env")

        #self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.llm = ChatOllama(model="qwen2.5:7b-instruct", temperature=0.2)

        # Đọc System Prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            self.system_prompt = "Bạn là tư vấn viên VinFast." # Fallback nếu lỗi đường dẫn

        # Khởi tạo bộ nhớ cho Agent (để nhớ các câu hỏi qua lại với khách)
        self.memory = MemorySaver()

        # Tạo ReAct Agent
        self.app = create_react_agent(
            model=self.llm,
            tools=agent_tools,
            checkpointer=self.memory
        )

    def _strip_thinking_tags(self, text: str) -> str:
        """Hàm dọn dẹp thẻ <thinking> trước khi hiển thị cho UI"""
        return re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL).strip()

    def get_response(self, user_question: str, session_id: str = "default_user") -> dict:
        """
        Dev 1 (UI) sẽ gọi hàm này. 
        - user_question: Lời nhắn của khách.
        - session_id: ID của phiên chat để LLM nhớ lịch sử (rất quan trọng trên giao diện Web).
        """
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            # Dùng stream để lấy log gọi tool real-time
            final_message = None
            for chunk in self.app.stream({"messages": [("system", self.system_prompt), ("user", user_question)]}, config=config, stream_mode="updates"):
                for node, values in chunk.items():
                    messages = values.get("messages", [])
                    if not messages:
                        continue
                        
                    last_msg = messages[-1] if isinstance(messages, list) else messages
                    
                    if node == "agent":
                        # Nếu AI trả về yêu cầu gọi tool
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            for tool in last_msg.tool_calls:
                                print(f"\n🔍 [AI Đang Thiết Lập]: Gọi công cụ '{tool['name']}'")
                                print(f"   📋 Đầu vào (Input): {tool['args']}")
                                
                    elif node == "tools":
                        print(f"✅ [Hệ Thống]: Đã nhận kết quả từ '{last_msg.name}'!\n")
                        
                    final_message = last_msg

            if final_message:
                raw_answer = final_message.content
                return {
                    "status": "ok",
                    "content": self._strip_thinking_tags(raw_answer)
                }
            return {
                "status": "error",
                "type": "empty_response",
                "message": "Không có nội dung trả về."
            }
            
        except TimeoutError:
            return {
                "status": "error",
                "type": "timeout",
                "message": "Hệ thống phản hồi quá lâu. Bạn vui lòng thử lại sau."
            }
            
        except Exception as e:
            return {
                "status": "error",
                "type": "unknown",
                "message": "Hệ thống đang gặp sự cố. Bạn vui lòng thử lại sau hoặc tham khảo website VinFast (https://vinfastauto.com)."
            }

# Export một instance duy nhất để các file khác import vào dùng
llm_agent = VinFastLLMHandler()
