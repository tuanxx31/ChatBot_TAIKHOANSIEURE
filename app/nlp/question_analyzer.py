from services.gpt_service import ChatGPTService
import json

class QuestionAnalyzer:
    def __init__(self):
        self.chatgpt = ChatGPTService()
        
    def analyze_and_respond(self, user_input: str, raw_data: dict = None) -> dict:
        """
        Phân tích câu hỏi và tạo câu trả lời trong một lần gọi GPT
        """
        system_prompt = """
        Bạn là một hệ thống chatbot thông minh. Hãy phân tích câu hỏi và tạo câu trả lời phù hợp.
        Trả về kết quả theo format JSON với các trường:
        - intent: loại câu hỏi (hỏi_gói_cước, hỏi_giá, hỏi_thông_tin, khác)
        - entity_type: loại đối tượng (product)
        - entity_name: tên sản phẩm
        - package_name: tên gói cước (nếu có)
        - confidence: độ tin cậy của phân tích (0-1)
        
        Chỉ trả về JSON, không thêm text khác.
        """
        
        # Tạo prompt phù hợp với từng trường hợp
        if raw_data is None:
            user_prompt = f"""
            Câu hỏi: {user_input}
            
            Hãy phân tích câu hỏi để xác định:
            1. Intent: hỏi_gói_cước, hỏi_giá, hỏi_thông_tin, hoặc khác
            2. Entity: tên sản phẩm
            3. Package: tên gói cước (nếu có)
            
            Nếu không tìm thấy entity hoặc không hiểu câu hỏi, trả về thông báo lỗi phù hợp.
            """
        else:
            user_prompt = f"""
            Câu hỏi: {user_input}
            Dữ liệu: {json.dumps(raw_data, ensure_ascii=False)}
            
            Hãy phân tích câu hỏi và tạo câu trả lời tự nhiên dựa trên dữ liệu được cung cấp.
            Nếu dữ liệu không phù hợp với câu hỏi, trả về thông báo lỗi phù hợp.
            """
        
        try:
            response = self.chatgpt.get_response(user_prompt, system_prompt)
            result = json.loads(response)
            
            # Đảm bảo các trường bắt buộc
            required_fields = ['intent', 'entity_type', 'entity_name', 'confidence']
            for field in required_fields:
                if field not in result:
                    if field == 'confidence':
                        result[field] = 0.0
                    else:
                        result[field] = None
            
            # Thêm package_name nếu chưa có
            if 'package_name' not in result:
                result['package_name'] = None
                    
            return result
            
        except Exception as e:
            print(f"Error analyzing question: {e}")
            # Trả về kết quả mặc định nếu có lỗi
            return {
                'intent': 'khác',
                'entity_type': 'product',
                'entity_name': None,
                'package_name': None,
                'confidence': 0.0
            } 