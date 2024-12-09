import streamlit as st
from assistant.prompt import get_intent_prompt, get_user_prompt, INTENT_LIST, SUB_PROMPT_LIST
from assistant.output_model import Output
from database.user_db import save_user
from assistant.knowledge_tags import knowledge_tags

API_KEY = st.secrets["API_KEY"]

from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

class Assistant:
    def __init__(self, user_info):
        self.user_info = user_info
        basic_llm = ChatOpenAI(api_key=API_KEY, temperature=0.2, model="gpt-4o-mini", verbose=False)
        self.helper = ChatOpenAI(api_key=API_KEY, temperature=0.7, model="gpt-4o-mini", verbose=False)
        self.model = "gpt-4o-mini"
        self.llm = basic_llm.with_structured_output(Output)
        if (self.user_info["chat_history"] == []):
            self.history_list = [{"role": "system", "content": "Bạn là một trợ lý hỗ trợ học môn Nhập môn lập trình. Hãy tuân thủ chặt chẽ các yêu cầu từ tôi."}]
        else:
            self.history_list = self.user_info["chat_history"]
        
    def get_intent(self, prompt: str):
        intent_prompt = get_intent_prompt(prompt)
        intent_message = [
            (
                "system",
                "Bạn là một trợ lý thông minh. Nhiệm vụ của bạn là phân loại ý định từ yêu cầu hoặc tin nhắn của người dùng theo đúng chính xác những gì được hướng dẫn, và hãy nhớ rằng luôn luôn trả lời bằng tiếng Việt."
            ),
            (
                "human",
                intent_prompt
            )
        ]
        with get_openai_callback() as cb:
            intent_response = self.helper.invoke(intent_message)
            intent = intent_response.content.strip()
            
        if intent not in INTENT_LIST:
            intent = "Không liên quan đến lập trình"

        return intent

    def update_level(self):
        if len(self.user_info["knowledge_list"]) >= 20:
            self.user_info["coding_level"] = "Chuyên nghiệp"
        elif len(self.user_info["knowledge_list"]) >= 10:
            self.user_info["coding_level"] = "Nâng cao"
        else:
            self.user_info["coding_level"] = "Cơ bản"
        return
    
    def get_sub_prompt(self, intent: str):
        switch_dict = {
            "Học kĩ năng lập trình mới": SUB_PROMPT_LIST[0],
            "Hướng dẫn giải quyết bài toán trong lập trình hoặc toán học": SUB_PROMPT_LIST[1],
            "Yêu cầu viết một đoạn code": SUB_PROMPT_LIST[2],
            "Yêu cầu sửa lỗi": SUB_PROMPT_LIST[3],
            "Hỏi liên quan đến vấn đề lập trình": SUB_PROMPT_LIST[4],
            "Không liên quan đến lập trình hay toán học": SUB_PROMPT_LIST[5]
        }    
        return switch_dict.get(intent, SUB_PROMPT_LIST[5])

    def get_user_prompt(self, user_info):
        user_prompt = get_user_prompt(user_info)
        return user_prompt

    def clear_chat_history(self):
        self.history_list.clear()
        self.history_list.append({"role": "system", "content": "Bạn là một trợ lý hỗ trợ học môn Nhập môn lập trình. Hãy tuân thủ chặt chẽ các yêu cầu từ tôi."})
        self.user_info["chat_history"] = self.history_list
        save_user(self.user_info)
        return
    
    def update_user_info(self, user_info):
        self.user_info = user_info
        save_user(self.user_info)
        return
    
    def update_knowledge_list(self, updated_knowledge):
        for tag in updated_knowledge:
            if tag not in self.user_info["knowledge_list"]:
                if tag == "Không liên quan đến lập trình hay toán học":
                    continue
                self.user_info["knowledge_list"].append(tag)
        return

    def get_knowledge_list(self):
        return self.user_info["knowledge_list"]


    def generate_response(self, prompt, user_info):
        self.user_info = user_info

        intent = self.get_intent(prompt)
        user_prompt = self.get_user_prompt(self.user_info)
        sub_prompt = self.get_sub_prompt(intent)

        full_prompt = f"[Yêu cầu]\n{prompt}\n[Hết yêu cầu]\n{user_prompt}\n{sub_prompt}"
        with get_openai_callback() as cb:
            if len(self.history_list) >= 4:
                summary_prompt = "Chắt lọc các tin nhắn trò chuyện bên dưới thành một tin nhắn tóm tắt duy nhất. Thêm càng nhiều chi tiết càng tốt. Đảm bảo rằng tin nhắn tóm tắt không bị thiếu thông tin quan trọng."
                # Thêm tất cả messages trong history_list thành một string
                for message in self.history_list:
                    summary_prompt += f"\n{message['role']}\n{message['content']}"
                summary_message = self.helper.invoke(summary_prompt).content
                self.history_list.clear()
                self.history_list.append({"role": "assistant", "content": summary_message})

            self.history_list.append({"role": "human", "content": full_prompt})
            structured_res = self.llm.invoke(self.history_list)
            self.history_list.append({"role": "assistant", "content": structured_res.response})
            self.user_info["chat_history"] = self.history_list
            
            self.update_knowledge_list(structured_res.tags)
            self.update_level()
            self.update_user_info(self.user_info)
            return structured_res.response