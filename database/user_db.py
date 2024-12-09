import streamlit as st
import os
import json

USER_DATA_FILE = st.secrets["USER_DATA_FILE"]

def save_user(user_info):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(user_info, file, indent=4, ensure_ascii=False)