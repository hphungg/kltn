def get_intent_prompt(prompt: str):
    return f"Phân loại ý định của yêu cầu sau đây theo các loại ý định được cung cấp. Chỉ trả về ý định được phân loại, không thêm bất cứ thông tin nào khác. Tuyệt đối không phân loại ý định nào khác ngoài các ý định được cung cấp. Chỉ phân loại vào loại ý định Học kĩ năng lập trình mới nếu yêu cầu cần biết một chủ đề liên quan tới kĩ năng lập trình như Biến, Mảng, Vòng lặp,... Các loại ý định bao gồm: 'Học kĩ năng lập trình mới', 'Hướng dẫn giải quyết bài toán trong lập trình hoặc toán học', 'Yêu cầu viết một đoạn code', 'Yêu cầu sửa lỗi', 'Hỏi liên quan đến lập trình', 'Không liên quan đến lập trình hay toán học'.\nYêu cầu từ người dùng: {prompt}"

def get_user_prompt(user_info):
    return f"Trả lời yêu cầu của tôi đưa ra phù hợp với thông tin và yêu cầu của tôi. Nếu đây là lần đầu trò chuyện, hãy chào tôi và giới thiệu bản thân trước khi trả lời. Thông tin của tôi như sau:\nTên: {user_info['name']}\nNgôn ngữ lập trình mong muốn trong trả lời: {user_info['coding_language']}\nMức độ kiến thức trong câu trả lời: {user_info['coding_level']}\nCác phần kiến thức tôi đã biết: {user_info['knowledge_list']}\n"

INTENT_LIST = [
    "Học kĩ năng lập trình mới",
    "Hướng dẫn giải quyết bài toán trong lập trình hoặc toán học",
    "Yêu cầu viết một đoạn code",
    "Yêu cầu sửa lỗi",
    "Hỏi liên quan đến vấn đề lập trình",
    "Không liên quan đến lập trình hay toán học"
]

LEARN_NEW_PROMPT = "Cung cấp các kiến thức liên quan tới yêu cầu trên. Nếu kiến thức liên quan tới các phần kiến thức đã học phía trên, gợi nhắc tôi về kiến thức đó. Câu trả lời cần bao gồm giới thiệu, các phần quan trọng và cung cấp một số ví dụ minh họa cho từng phần kiến thức đó. Không cần cung cấp phần giải thích, ứng dụng hay kết luận gì khác trừ khi trong yêu cầu có đề cập tới. Luôn trả lời bằng tiếng Việt."

HELP_CODE_PROMPT = "Cung cấp hướng dẫn chi tiết bằng tiếng Việt theo từng bước để giải quyết yêu cầu đã đưa ra. Hãy suy nghĩ từng bước một để đảm bảo bạn có câu trả lời chính xác nhất. Tuyệt đối không cung cấp đoạn code hoặc hàm code trong câu trả lời nếu không có trong yêu cầu. Câu trả lời không được chứa kí hiệu latex nào. Câu trả lời nên sử dụng các kiến thức tôi đã học, nếu cần phần kiến thức nào đó mới để giải quyết, thêm ngắn gọn phần gợi ý các kiến thức đó phía dưới cùng câu trả lời. \n[Ví dụ yêu cầu]\nCách tìm ước chung lớn nhất của hai số nguyên dương a và b. \n[Ví dụ câu trả lời theo từng bước]\nCác bước giải quyết bài toán: \nBước 1: Ước là các nguyên mà một nguyên khác có thể chia hết cho nó. Một số được gọi là ước chung của hai hay nhiều số nếu nó là ước của tất cả các số đó. \nBước 2: Các số nguyên i thỏa mãn là ước chung của a và b phải thỏa mãn yêu cầu 0 < i <= min(a, b) và a, b đều chia hết cho i. \nBước 3: Kiểm tra tất cả các số nguyên i nhỏ hơn a và b bằng một vòng lặp, kiểm tra điều kiện chia hết bằng một câu lệnh if \nBước 4: Lưu lại số nguyên i thỏa mãn lớn nhất trong quá trình tìm kiếm. \nBước 5: In ra kết quả vừa lưu tìm được."

WRITE_CODE_PROMPT = "Cung cấp đoạn code giải quyết đầy đủ yêu cầu đã đưa ra. Đoạn code không được chứa ví dụ để sử dụng mà chỉ nên chứa những hàm chính. Nếu đoạn code trả lời chứa nhiều hàm hoặc nhiều phần code riêng biệt, hãy chia thành nhiều phần code khác nhau và cung cấp giải thích bằng tiếng Việt cho từng phần trong đoạn code đó. Đảm bảo đoạn code trả lời không chứa lỗi cú pháp và có thể chạy được. Đoạn code bắt buộc phải là ngôn ngữ lập trình mà tôi mong muốn phía trên."

FIX_BUG_PROMPT = "Tìm ra lỗi trong yêu cầu đưa ra và cung cấp giải pháp sửa lỗi. Chỉ rõ ràng đây là lỗi gì và nguyên nhân thường gặp lỗi này, và cung cấp một giải pháp tối ưu nhất để sửa lỗi đó. Đảm bảo giải pháp sửa lỗi không chứa lỗi cú pháp và có thể chạy được. Đoạn code bắt buộc phải là ngôn ngữ lập trình mà tôi mong muốn phía trên. Đưa ra câu hỏi xem người dùng có thắc mắc gì không hoặc muốn giải pháp sửa lỗi khác không."

ASK_PROGRAMMING_PROMPT = "Cung cấp câu trả lời chi tiết cho yêu cầu đưa ra. Câu trả lời chỉ cần trả lời nội dung chính, không thêm phần giới thiệu hoặc kết luận, hoặc các phần ví dụ không liên quan trừ khi được nhắc đến trong yêu cầu. Luôn trả lời bằng tiếng Việt. Câu trả lời nên sử dụng các kiến thức tôi đã học, nếu cần phần kiến thức nào đó mới để giải quyết, thêm ngắn gọn phần gợi ý các kiến thức đó phía dưới cùng câu trả lời."

NOT_RELATED_PROMPT = "Nếu yêu cầu đưa ra liên quan đến các câu hỏi và trả lời trước đó, trả lời theo yêu cầu đưa ra một cách chi tiết hơn các câu trả lời trước, có thể tăng mức độ trả lời đã đưa ra. Nếu yêu cầu liên quan tới nhắc lại các yêu cầu trước đó, hãy chỉ đưa ra phần yêu cầu chính, chứ không đề cập tới các thông tin cung cấp thêm.\n Nếu yêu cầu đưa ra không liên quan đến cuộc trò chuyện trước đó hoặc không liên quan đến lập trình, hãy xin lỗi tôi, trả lời ngắn gọn yêu cầu đưa ra của người dùng và sau đó chuyển hướng đề tài về các chủ đề khác liên quan đến lập trình. Luôn trả lời bằng tiếng Việt."

SUB_PROMPT_LIST = [
    LEARN_NEW_PROMPT,
    HELP_CODE_PROMPT,
    WRITE_CODE_PROMPT,
    FIX_BUG_PROMPT,
    ASK_PROGRAMMING_PROMPT,
    NOT_RELATED_PROMPT
]

