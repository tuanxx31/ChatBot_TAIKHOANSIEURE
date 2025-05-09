class IntentAnalyzer:
    def __init__(self):
        # Sử dụng các từ khóa đơn giản thay vì GPT để phân tích intent
        self.intent_keywords = {
            'price': ['giá', 'bao nhiêu', 'chi phí', 'phí', 'mất bao nhiêu'],
            'description': ['là gì', 'mô tả', 'giới thiệu', 'có gì', 'gồm những gì'],
            'availability': ['có không', 'còn không', 'có sẵn', 'khi nào có'],
            'contact': ['liên hệ', 'số điện thoại', 'email', 'địa chỉ']
        }
    
    def analyze(self, user_input: str) -> str:
        """
        Phân tích intent của câu hỏi dựa trên từ khóa
        """
        user_input = user_input.lower()
        
        # Kiểm tra từng intent và từ khóa
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                return intent
                
        return 'general'  # Intent mặc định nếu không tìm thấy 