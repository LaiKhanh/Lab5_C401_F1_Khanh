from langgraph.graph import StateGraph, END
from typing import TypedDict

from modules.validator import handle_exception
from modules.llm_handler import llm_agent




# ===== STATE =====
class AgentState(TypedDict):
    input: str
    clean_input: str
    response: str


# ===== NODE 1: VALIDATOR =====
def validator_node(state: AgentState):
    result = handle_exception(state["input"])

    if result["status"] != "ok":
        return {
            "response": result["message"]
        }

    return {
        "clean_input": result["cleaned_input"]
    }


def route_after_validator(state):
    if "response" in state:
        return END
    return "llm"


# ===== NODE 2: LLM =====
def llm_node(state: AgentState):
    user_input = state["clean_input"]

    result = llm_agent.get_response(user_input, session_id="cli_user")

    if result["status"] != "ok":
        return {
            "response": result["message"]
        }

    return {
        "response": result["content"]
    }


# ===== GRAPH =====
builder = StateGraph(AgentState)

builder.add_node("validator", validator_node)
builder.add_node("llm", llm_node)

builder.set_entry_point("validator")

builder.add_conditional_edges(
    "validator",
    route_after_validator,
    {
        "llm": "llm",
        END: END
    }
)

builder.add_edge("llm", END)

graph = builder.compile()


# ===== CLI TEST =====
if __name__ == "__main__":
    print("=== VinFast AI Assistant ===")

    while True:
        user_input = input("\nBạn: ")

        if user_input.lower() == "exit":
            break

        result = graph.invoke({
            "input": user_input
        })

        if "response" in result:
            print("\nBot:", result["response"])
        else:
            print("\nBot: Hệ thống không trả về phản hồi hợp lệ.")