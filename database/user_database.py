import json
import os

USER_DATA_FILE = "user_data.json"

def save_user_data(user_info):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(user_info, file, indent=4, ensure_ascii=False)

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {
        "name": "",
        "coding_strength": "",
        "coding_level": "Cơ bản",
        "coding_language": "C++",
        "knowledge_list": [],
        "solved_quest_tag": [],
        "chat_history": []
    }
