import streamlit as st
import os
import json

from assistant.assistant import Assistant
from core.sg_knowledge_query import knowledge_query
from core.sg_question_query import question_query

from database.history_manager import load_chat_history, save_chat_history
from database.knowledge_db import Neo4jConnector
from database.question_db import MongoDBConnector

USER_DATA_FILE = st.secrets["USER_DATA_FILE"] + "_1.json"

st.set_page_config(page_title="Lập trình hướng đối tượng", page_icon="🤖")

def new_user_data():
    return {
        "name": "",
        "coding_strength": "",
        "coding_level": "Cơ bản",
        "coding_language": "C++",
        "knowledge_list": [],
        "solved_quest_tag": [],
        "chat_history": []
    }
    
@st.cache_resource
def load_assistant(user_info, user_data_file):
    return Assistant(user_info, user_data_file)

@st.cache_resource
def load_graphdb():
    return Neo4jConnector()

@st.cache_resource
def load_mongo():
    return MongoDBConnector()  

@st.cache_resource
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return new_user_data()

user_info = load_user_data()
graph_db = load_graphdb()
mongo_db = load_mongo()
assistant = load_assistant(user_info, USER_DATA_FILE)

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history("2")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

knowledge_suggestions = knowledge_query(assistant.get_knowledge_list(), graph_db)
question_suggestions = question_query(assistant.get_knowledge_list(), mongo_db)

def handle_knowledge_suggestion(suggestion):
    my_prompt = f"Tôi muốn tìm hiểu về {suggestion.lower()}"
    st.session_state.messages.append({"role": "user", "content": my_prompt})
    full_response = assistant.generate_response(my_prompt, user_info)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_chat_history(st.session_state.messages, "2")

def handle_question_suggestion(question):
    quest_content = f"Viết chương trình giải bài tập sau đây:\n### {question["title"]}\n\n{question["content"]}"
    st.chat_message("assistant").markdown(quest_content)
    st.session_state.messages.append({"role": "assistant", "content": quest_content})

if (("messages" not in st.session_state) or (len(st.session_state.messages) == 0)):
    st.header("🤖 Lập trình hướng đối tượng")
    st.markdown(
        "Đây là trợ lý hỗ trợ học tập môn Lập trình hướng đối tượng. "
        "Hãy đưa ra một yêu cầu hoặc lựa chọn các gợi ý học tập để bắt đầu cuộc trò chuyện."
    )
    st.subheader("Bắt đầu bằng cách tìm hiểu một trong những chủ đề sau:")
    for i, suggestion in enumerate(knowledge_suggestions):
        st.button(suggestion, key=f"start_ks_{i}", on_click=lambda s=suggestion: handle_knowledge_suggestion(s))
    st.subheader("Hoặc có thể luyện tập với một trong các bài tập sau:")
    for i, question in enumerate(question_suggestions):
        st.button(question["title"], key=f"start_qs_{i}", on_click=lambda s=suggestion: handle_question_suggestion(s))

# Sidebar
st.sidebar.header("Gợi ý chủ đề học tiếp theo")
for i, suggestion in enumerate(knowledge_suggestions):
    st.sidebar.button(suggestion, key=f"side_ks_{i}", on_click=lambda s=suggestion: handle_knowledge_suggestion(s))
st.sidebar.header("Gợi ý bài tập luyện tập")
for i, question in enumerate(question_suggestions):
    st.sidebar.button(question["title"], key=f"side_qs_{i}", on_click=lambda s=suggestion: handle_question_suggestion(s))

st.sidebar.header("Thông tin cá nhân")
st.sidebar.markdown("Bạn có thể cung cấp thông tin cá nhân của bạn để trợ lý có thể cung cấp câu trả lời phù hợp và chính xác hơn.")

user_info["name"] = st.sidebar.text_input("Tên của bạn:", user_info["name"])
user_info["coding_language"] = st.sidebar.selectbox("Ngôn ngữ lập trình:", ["C++", "Python", "Java", "JavaScript"], index=["C++", "Python", "Java", "JavaScript"].index(user_info["coding_language"]))
user_info["coding_level"] = st.sidebar.selectbox("Mức độ của câu trả lời từ trợ lý:", ["Cơ bản", "Nâng cao", "Chuyên nghiệp"], index=["Cơ bản", "Nâng cao", "Chuyên nghiệp"].index(user_info["coding_level"]))

# Xử lý xóa dữ liệu trò chuyện
def clear_history():
    st.session_state.messages = []
    assistant.clear_chat_history()
    save_chat_history([], "2")

def clear_all_history():
    st.session_state.messages = []
    assistant.clear_chat_history()
    user_info = new_user_data()
    assistant.update_user_info(user_info)
    save_chat_history([], "2")

with st.sidebar:
    st.button("Xóa dữ liệu trò chuyện hiện tại", on_click=clear_history)
    st.button("Xóa toàn bộ dữ liệu", on_click=clear_all_history)

# Người dùng nhập câu hỏi
if prompt := st.chat_input("Hỏi một câu hỏi nào đó"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = assistant.generate_response(prompt, user_info)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_chat_history(st.session_state.messages, "2")
    


