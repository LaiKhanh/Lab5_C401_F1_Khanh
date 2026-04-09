import streamlit as st
from datetime import datetime
import json
import os
from datetime import datetime as dt

REPORT_FILE = "data/reports.json"

def init_report_file():
    """Khởi tạo file reports.json nếu chưa tồn tại"""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def save_report(message_content: str, reason: str):
    """Lưu report vào file JSON"""
    init_report_file()
    reports = []
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            reports = json.load(f)
    
    new_report = {
        "timestamp": dt.now().strftime("%d/%m/%Y %H:%M:%S"),
        "message": message_content,
        "reason": reason
    }
    reports.append(new_report)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)

def inject_custom_css():
    """Nhúng CSS để fix màu Palette, cố định Header và tối ưu khung nhập liệu"""
    COLOR_MAIN_BG = "#F3F8FF"
    COLOR_BOT_BUBBLE = "#DEECFF"
    COLOR_USER_BUBBLE = "#C6CFFF"
    COLOR_ACCENT_HOVER = "#E8D3FF"
    COLOR_SIDEBAR_NAVY = "#172B53"
    COLOR_YELLOW_BTN = "#FFEB3B"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
        background-color: {COLOR_MAIN_BG} !important;
    }}

    [data-testid="stHeader"] {{ 
        display: flex !important; 
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1000px !important;
        padding: 100px 1rem 150px 1rem !important;
        margin: 0 auto !important;
    }}

    /* FIXED HEADER */
    .nav-title {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        background-color: {COLOR_MAIN_BG} !important;
        border-bottom: 2px solid {COLOR_ACCENT_HOVER} !important;
        padding: 15px 0 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        color: {COLOR_SIDEBAR_NAVY} !important;
        text-align: center !important;
        z-index: 99 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }}

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background-color: {COLOR_SIDEBAR_NAVY} !important;
        border-right: 2px solid {COLOR_ACCENT_HOVER} !important;
    }}

    .sidebar-title {{ font-size: 22px; font-weight: 800; color: white; text-align: center; margin: 20px 0; }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        background-color: transparent;
        border: none;
        color: rgba(255,255,255,0.7);
        padding: 12px 20px;
        text-align: left;
        justify-content: flex-start;
        font-weight: 500;
        margin-bottom: 8px;
    }}

    .new-chat-container .stButton > button {{
        background-color: {COLOR_YELLOW_BTN} !important;
        color: {COLOR_SIDEBAR_NAVY} !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        justify-content: center !important;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: {COLOR_ACCENT_HOVER} !important;
        color: {COLOR_SIDEBAR_NAVY} !important;
        font-weight: 700 !important;
    }}

    /* CHAT MESSAGES */
    .chat-container {{ display: flex; flex-direction: column; gap: 25px; margin-top: 20px; }}
    .msg-wrapper {{ display: flex; gap: 15px; max-width: 85%; align-items: flex-start; }}
    .msg-wrapper.bot {{ align-self: flex-start; justify-content: flex-start; }}
    .msg-wrapper.user {{ align-self: flex-end; flex-direction: row-reverse; }}
    .avatar {{ font-size: 24px; flex-shrink: 0; padding-top: 5px; }}
    .msg-content {{ display: flex; flex-direction: column; gap: 5px; }}
    .bubble {{ padding: 14px 18px; border-radius: 15px; font-size: 15px; line-height: 1.5; }}
    .bot .bubble {{ background-color: {COLOR_BOT_BUBBLE}; color: {COLOR_SIDEBAR_NAVY}; border-top-left-radius: 2px; }}
    .user .bubble {{ background-color: {COLOR_USER_BUBBLE}; color: {COLOR_SIDEBAR_NAVY}; border-top-right-radius: 2px; }}
    .msg-actions {{ display: flex; gap: 10px; }}
    .msg-more-btn {{ background: none; border: none; font-size: 18px; cursor: pointer; color: {COLOR_SIDEBAR_NAVY}; padding: 0; }}
    .msg-more-btn:hover {{ opacity: 0.7; }}
    .report-menu {{ display: flex; gap: 8px; }}
    .report-btn {{ background-color: #FF6B6B; color: white; border: none; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600; }}
    .report-btn:hover {{ background-color: #FF5252; }}

    /* TỐI ƯU KHUNG NHẬP LIỆU (PROMPT INPUT) */
    [data-testid="stForm"] {{
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 85% !important;
        max-width: 850px !important;
        height: 70px !important;
        background-color: white !important;
        border: 2px solid {COLOR_ACCENT_HOVER} !important;
        border-radius: 20px !important;
        padding: 0 15px !important;
        z-index: 100 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Fix lệch cho màn hình desktop có sidebar */
    @media (min-width: 768px) {{
        [data-testid="stForm"] {{ left: calc(50% + 130px) !important; }}
    }}

    [data-testid="stForm"] .stHorizontalBlock {{
        width: 100% !important;
        align-items: center !important;
    }}

    /* Làm sạch ô input */
    [data-testid="stTextInput"] input {{
        background-color: transparent !important;
        border: none !important;
        padding: 10px 0 !important;
        color: {COLOR_SIDEBAR_NAVY} !important;
    }}

    /* Chỉnh nút SEND cho đẹp */
    [data-testid="stFormSubmitButton"] > button {{
        background-color: {COLOR_SIDEBAR_NAVY} !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 20px !important;
        font-weight: 700 !important;
        transition: transform 0.2s;
    }}
    
    [data-testid="stFormSubmitButton"] > button:hover {{
        transform: scale(1.05);
        background-color: #243b6d !important;
    }}
    </style>
    <div class="nav-title">ViVin Chatbot</div>
    """, unsafe_allow_html=True)

REPORT_REASONS = [
    "Câu trả lời không chính xác",
    "Câu trả lời không liên quan",
    "Câu trả lời khiến tôi bị lầm lẫn",
    "Câu trả lời không đủ chi tiết",
    "Lỗi kỹ thuật/máy chủ",
    "Khác"
]

@st.dialog("📋 Báo cáo câu trả lời")
def render_report_modal(message_index: int, message_content: str):
    """Hàm hiển thị modal popup để chọn lý do report"""
    st.markdown("""
    <style>
        [data-testid="stDialog"] {
            background-color: white !important;
        }
        .dialog-title {
            color: #172B53;
            font-weight: 700;
            font-size: 20px;
            margin-bottom: 15px;
        }
        .dialog-label {
            color: #172B53;
            font-weight: 600;
            margin-bottom: 10px;
            display: block;
            font-size: 14px;
        }
        [data-testid="stDialog"] [data-testid="stRadio"] {
            background: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<span class="dialog-label">Chọn lý do báo cáo:</span>', unsafe_allow_html=True)
    
    # Radio buttons
    selected_reason = st.radio(
        "Lý do:",
        REPORT_REASONS,
        key=f"report_reason_{message_index}",
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Hủy", use_container_width=True, key=f"cancel_report_{message_index}"):
            st.session_state.report_modal = None
            st.rerun()
    with col2:
        if st.button("✓ Gửi", use_container_width=True, key=f"send_report_{message_index}"):
            try:
                # Save the report to file
                save_report(message_content, selected_reason)
                st.success("✓ Báo cáo đã được gửi thành công!")
                # Close modal after successful save
                st.session_state.report_modal = None
                import time
                time.sleep(0.5)  # Brief pause to show success message
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi gửi báo cáo: {str(e)}")

def render_sidebar_content():
    """Hàm vẽ nội dung bên trong sidebar"""
    st.markdown('<div class="sidebar-title">VIVIN</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
    if st.button("New Chat", use_container_width=True, key="side_new_chat"):
        if len(st.session_state.messages) > 1:
            st.session_state.chat_history.append({
                "time": datetime.now().strftime("%H:%M - %d/%m"),
                "messages": st.session_state.messages.copy()
            })
        st.session_state.messages = [{"role": "bot", "content": "ViVin xin chào, anh/chị đang có nhu cầu mua loại xe nào?"}]
        st.session_state.current_page = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    chat_type = "primary" if st.session_state.current_page == "chat" else "secondary"
    if st.button("Current Chat", type=chat_type, use_container_width=True, key="side_curr"):
        st.session_state.current_page = "chat"
        st.rerun()

    hist_type = "primary" if st.session_state.current_page == "history" else "secondary"
    if st.button("History", type=hist_type, use_container_width=True, key="side_hist"):
        st.session_state.current_page = "history"
        st.rerun()

    acc_type = "primary" if st.session_state.current_page == "account" else "secondary"
    if st.button("Account", type=acc_type, use_container_width=True, key="side_acc"):
        st.session_state.current_page = "account"
        st.rerun()
