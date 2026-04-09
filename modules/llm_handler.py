<<<<<<< HEAD
import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Import list công cụ từ file tools.py của bạn
from tools.tools import agent_tools

class VinFastLLMHandler:
    def __init__(self):
        load_dotenv()
        if not os.environ.get("OPENAI_API_KEY"):
            print("CẢNH BÁO: Chưa có OPENAI_API_KEY trong file .env")

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        
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
            state_modifier=SystemMessage(content=self.system_prompt),
            checkpointer=self.memory
        )

    def _strip_thinking_tags(self, text: str) -> str:
        """Hàm dọn dẹp thẻ <thinking> trước khi hiển thị cho UI"""
        return re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL).strip()

    def get_response(self, user_question: str, session_id: str = "default_user") -> str:
        """
        Dev 1 (UI) sẽ gọi hàm này. 
        - user_question: Lời nhắn của khách.
        - session_id: ID của phiên chat để LLM nhớ lịch sử (rất quan trọng trên giao diện Web).
        """
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            result = self.app.invoke(
                {"messages": [("user", user_question)]},
                config=config
            )
            
            raw_answer = result["messages"][-1].content
            return self._strip_thinking_tags(raw_answer)
            
        except Exception as e:
            return f"Xin lỗi, hệ thống AI đang bảo trì. Chi tiết lỗi: {e}"

# Export một instance duy nhất để các file khác import vào dùng
llm_agent = VinFastLLMHandler()
=======
from langchain_ollama import ChatOllama

MODEL_NAME = "qwen2.5:7b-instruct"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        temperature=0.3
    )

# A wrapper around LLM invocation to handle exceptions gracefully
def llm_invoke(llm, prompt: str):
    try:
        response = llm.invoke(prompt)

        return {
            "status": "ok",
            "content": response.content
        }

    except Exception as e:
        return {
            "status": "error",
            "type": "llm_failure",
            "message": "Hệ thống đang bận hoặc gặp lỗi khi xử lý. Bạn thử lại sau nhé."
        }
>>>>>>> 9421bed83b23e8d3ac18805314c4ffbd3d48df74
