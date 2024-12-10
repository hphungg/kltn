import json

def save_user(user_info, user_data_file):
    with open(user_data_file, "w", encoding="utf-8") as file:
        json.dump(user_info, file, indent=4, ensure_ascii=False)