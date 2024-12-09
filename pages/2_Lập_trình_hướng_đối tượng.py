import streamlit as st
from assistant.assistant import Assistant
from core.study_suggestions import query_suggestions
from database.cache_manager import load_chat_history, save_chat_history
from database.user_database import load_user_data, save_user_data

st.set_page_config(page_title="Lập trình hướng đối tượng", page_icon="🤖")

@st.cache_resource
def load_assistant(user_info):
    # Truyền thông tin người dùng vào Assistant
    return Assistant(user_info)

# Tải thông tin người dùng
user_info = load_user_data()

# Tải trợ lý với thông tin người dùng
assistant = load_assistant(user_info)

def handle_assistant_response(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    response = assistant.generate_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    save_chat_history(st.session_state.messages)

def button_click(suggestion):
    st.session_state["user_input"] = f"Tôi muốn tìm hiểu về {suggestion.lower()}"
    handle_assistant_response(st.session_state["user_input"])
    st.rerun()

if ("messages" not in st.session_state) or (st.session_state["messages"] == []):
    st.header("🤖 Nhập môn lập trình")
    st.markdown(
        "Đây là trợ lý hỗ trợ học tập môn Nhập môn lập trình. "
        "Hãy đưa ra một yêu cầu hoặc lựa chọn các gợi ý học tập để bắt đầu cuộc trò chuyện."
    )

# Tải lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history() 

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Hiển thị lịch sử trò chuyện
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Sidebar
st.sidebar.title("Thông tin cá nhân")
st.sidebar.markdown("Cung cấp thông tin cá nhân của bạn để trợ lý có thể cung cấp câu trả lời phù hợp hơn.")

updated_name = st.sidebar.text_input("Tên của bạn:", user_info["name"])
updated_coding_language = st.sidebar.selectbox(
    "Ngôn ngữ lập trình:", 
    ["C++", "Python", "Java", "JavaScript"], 
    index=["C++", "Python", "Java", "JavaScript"].index(user_info["coding_language"])
)
updated_coding_level = st.sidebar.selectbox(
    "Mức độ của câu trả lời từ trợ lý:", 
    ["Cơ bản", "Nâng cao", "Chuyên nghiệp"], 
    index=["Cơ bản", "Nâng cao", "Chuyên nghiệp"].index(user_info["coding_level"])
)

with st.sidebar:
    if st.button("Xóa dữ liệu trò chuyện hiện tại"):
        st.session_state.messages = []
        assistant.clear_chat_history()
        save_chat_history([])
        st.rerun()

suggestions = query_suggestions(assistant.get_knowledge_list())

st.sidebar.header("Gợi ý chủ đề học tiếp theo")
for suggestion in suggestions:
    st.sidebar.button(suggestion, on_click=button_click, args=(suggestion,))


# Kiểm tra nếu thông tin thay đổi, lưu lại
if (
    updated_name != user_info["name"] or
    updated_coding_level != user_info["coding_level"] or
    updated_coding_language != user_info["coding_language"]
):
    user_info["name"] = updated_name
    user_info["coding_level"] = updated_coding_level
    user_info["coding_language"] = updated_coding_language
    assistant.update_user_info(user_info)

if prompt := st.chat_input("Hỏi một câu hỏi nào đó"):
    handle_assistant_response(prompt)
    st.rerun()
