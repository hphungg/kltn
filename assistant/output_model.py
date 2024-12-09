from pydantic import BaseModel, Field
from typing import List
from assistant.knowledge_tags import knowledge_tags

class Output(BaseModel):
    response: str = Field(description="Toàn bộ câu trả lời của trợ lý.")
    tags: List[str] = Field(description=f"Danh sách các nhãn liên quan tới kiến thức được đề cập trong nội dung của câu trả lời. Bắt buộc phải là các giá trị nằm trong danh sách sau đây {knowledge_tags}. Tuyệt đối không được tạo ra một nhãn mới.")
    level: str = Field(description="Mức độ của câu trả lời, bắt buộc phải là 1 trong 3 lựa chọn: 'Cơ bản', 'Nâng cao' hoặc 'Chuyên nghiệp'.")