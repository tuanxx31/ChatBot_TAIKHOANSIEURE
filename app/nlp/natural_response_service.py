from services.gpt_service import ChatGPTService

class NaturalResponseService:
    def __init__(self):
        self.chatgpt = ChatGPTService()

    def from_data(self, structured_text: str) -> str:
        """
        Tạo câu trả lời tự nhiên từ dữ liệu có cấu trúc
        """
        system_prompt = (
            "Bạn là nhân viên tư vấn sản phẩm. "
            "Hãy viết lại thông tin dưới đây thành đoạn mô tả tự nhiên, "
            "ngắn gọn, dễ hiểu, mang tính thuyết phục. "
            "Chỉ sử dụng thông tin được cung cấp, không thêm thông tin khác."
        )
        return self.chatgpt.get_response(structured_text, system_prompt=system_prompt)
