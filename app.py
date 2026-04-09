import streamlit as st
import time
from modules.ui_components import inject_custom_css, render_sidebar_content, render_report_modal
from modules.llm_handler import llm_agent
from modules.validator import handle_exception

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Vivin Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "content": "ViVin xin chào, anh/chị đang có nhu cầu mua loại xe nào?"}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"
if "loading" not in st.session_state:
    st.session_state.loading = False
if "report_modal" not in st.session_state:
    st.session_state.report_modal = None

# 3. SETUP CSS & HEADER
inject_custom_css()

# 4. SIDEBAR
with st.sidebar:
    render_sidebar_content()

# 5. PAGE CONTENT
if st.session_state.current_page == "chat":
    # Hiển thị modal nếu có
    if st.session_state.report_modal is not None:
        msg_content = st.session_state.messages[st.session_state.report_modal]["content"]
        render_report_modal(st.session_state.report_modal, msg_content)
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for idx, msg in enumerate(st.session_state.messages):
        role_class = "bot" if msg["role"] == "bot" else "user"
        icon = "🤖" if msg["role"] == "bot" else "👤"
        
        if msg["role"] == "bot":
            # Hiển thị bot message với button report
            st.markdown(f"""
                <div class="msg-wrapper {role_class}">
                    <div class="avatar">{icon}</div>
                    <div class="msg-content">
                        <div class="bubble">{msg['content']}</div>
                        <div class="msg-subtext">ViVin</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Thêm button "..." để report
            col1, col2 = st.columns([0.85, 0.15])
            with col2:
                if st.button("⋯", key=f"more_btn_{idx}", help="Thêm lựa chọn"):
                    if st.session_state.report_modal == idx:
                        st.session_state.report_modal = None
                    else:
                        st.session_state.report_modal = idx
                    st.rerun()
        else:
            # Hiển thị user message bình thường
            st.markdown(f"""
                <div class="msg-wrapper {role_class}">
                    <div class="avatar">{icon}</div>
                    <div class="msg-content">
                        <div class="bubble">{msg['content']}</div>
                        <div class="msg-subtext">YOU</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    if st.session_state.loading:
        st.markdown('<div class="msg-wrapper bot"><div class="avatar">🤖</div><div class="bubble">...</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Khung nhập liệu tối ưu
    with st.form(key="chat_input_final", clear_on_submit=True):
        cols = st.columns([0.88, 0.12])
        user_msg = cols[0].text_input("Input", placeholder="Hỏi ViVin tại đây...", label_visibility="collapsed")
        submit = cols[1].form_submit_button("SEND")

    if submit and user_msg:
        check = handle_exception(user_msg)
        if check["status"] == "ok":
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.loading = True
            st.rerun()
        else:
            st.error(check["message"])

elif st.session_state.current_page == "history":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("📋 Lịch sử trò chuyện")
    if not st.session_state.chat_history:
        st.info("Chưa có lịch sử trò chuyện.")
    else:
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Hội thoại ngày {chat['time']}"):
                for m in chat['messages']:
                    st.write(f"**{m['role'].upper()}**: {m['content']}")

elif st.session_state.current_page == "account":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("👤 Thông tin cá nhân")
    st.info("Tính năng đang được cập nhật.")

# 6. AI RESPONSE LOGIC
if st.session_state.loading:
    time.sleep(0.5)
    last_user_msg = st.session_state.messages[-1]["content"]
    response = llm_agent.get_response(last_user_msg, session_id="session_f1")

    if response["status"] != "ok":
        bot_message = response["message"]
    else:
        bot_message = response["content"]

    st.session_state.messages.append({"role": "bot", "content": bot_message})
    st.session_state.loading = False
    st.rerun()
