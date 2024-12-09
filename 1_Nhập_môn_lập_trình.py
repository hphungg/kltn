import streamlit as st
from assistant.assistant import Assistant
from core.study_suggestions import query_suggestions
from core.ques_suggestions import query_questions
from database.cache_manager import load_chat_history, save_chat_history
from database.user_database import load_user_data, save_user_data

st.set_page_config(page_title="Nhập môn lập trình", page_icon="🤖")

@st.cache_resource
def load_assistant(user_info):
    return Assistant(user_info)

user_info = load_user_data()
assistant = load_assistant(user_info)

if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history()

if "selected_suggestion" not in st.session_state:
    st.session_state["selected_suggestion"] = None

if "selected_quest" not in st.session_state:
    st.session_state["selected_quest"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


def handle_assistant_response(user_input):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = assistant.generate_response(user_input)
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    save_chat_history(st.session_state.messages)
    st.session_state["selected_suggestion"] = None
    st.rerun()

suggestions = query_suggestions(assistant.get_knowledge_list())
ques_suggestions = query_questions(assistant.get_knowledge_list())

if len(st.session_state.messages) == 0:
    st.header("🤖 Nhập môn lập trình")
    st.markdown(
        "Đây là trợ lý hỗ trợ học tập môn Nhập môn lập trình. "
        "Hãy đưa ra một yêu cầu hoặc lựa chọn các gợi ý học tập để bắt đầu cuộc trò chuyện."
    )
    st.subheader("Bắt đầu bằng cách tìm hiểu một trong những chủ đề sau:")
    for suggestion in suggestions:
        if st.button(suggestion):
            st.session_state["selected_suggestion"] = suggestion
    st.subheader("Hoặc có thể luyện tập với một trong các bài tập sau:")
    for question in ques_suggestions:
        if st.button(question["title"]):
            st.session_state["selected_quest"] = question

# Sidebar

st.sidebar.header("Gợi ý chủ đề học tiếp theo")
for suggestion in suggestions:
    if st.sidebar.button(suggestion, key=suggestion):
        st.session_state["selected_suggestion"] = suggestion

if st.session_state["selected_suggestion"] is not None:
    my_prompt = f"Tôi muốn tìm hiểu về {st.session_state["selected_suggestion"].lower()}"
    handle_assistant_response(my_prompt)

if st.session_state["selected_quest"] is not None:
    quest_content = f"## {st.session_state["selected_quest"]["title"]}\n\n{st.session_state["selected_quest"]["content"]}"
    st.chat_message("assistant").write(quest_content)
    st.session_state["selected_quest"] = None


st.sidebar.header("Thông tin cá nhân")
st.sidebar.markdown("Bạn có thể cung cấp thông tin cá nhân của bạn để trợ lý có thể cung cấp câu trả lời phù hợp và chính xác hơn.")

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

# Xử lý xóa dữ liệu trò chuyện
with st.sidebar:
    if st.button("Xóa dữ liệu trò chuyện hiện tại"):
        st.session_state.messages = []
        assistant.clear_chat_history()
        save_chat_history([])  # Lưu lại lịch sử trống
        st.rerun()

# Kiểm tra nếu thông tin người dùng thay đổi và cập nhật
if (
    updated_name != user_info["name"] or
    updated_coding_level != user_info["coding_level"] or
    updated_coding_language != user_info["coding_language"]
):
    user_info["name"] = updated_name
    user_info["coding_level"] = updated_coding_level
    user_info["coding_language"] = updated_coding_language
    assistant.update_user_info(user_info)

# Xử lý đầu vào của người dùng qua trường nhập liệu chat
if prompt := st.chat_input("Hỏi một câu hỏi nào đó"):
    handle_assistant_response(prompt)
