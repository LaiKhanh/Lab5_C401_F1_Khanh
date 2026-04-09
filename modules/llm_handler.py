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
