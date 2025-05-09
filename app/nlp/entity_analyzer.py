class EntityAnalyzer:
    def __init__(self):
        # Danh sách các entity type và từ khóa nhận dạng
        self.entity_types = {
            'product': ['capcut', 'premiere', 'after effects', 'photoshop'],
            'company': ['công ty', 'công ty chúng tôi', 'chúng tôi', 'công ty mình'],
            'service': ['dịch vụ', 'hỗ trợ', 'tư vấn']
        }
        
    def analyze(self, user_input: str) -> dict:
        """
        Phân tích entity từ câu hỏi
        """
        user_input = user_input.lower()
        
        # Tìm entity type
        entity_type = 'product'  # Mặc định là product
        for type_name, keywords in self.entity_types.items():
            if any(keyword in user_input for keyword in keywords):
                entity_type = type_name
                break
                
        # Tìm entity name
        entity_name = None
        if entity_type == 'product':
            for product in self.entity_types['product']:
                if product in user_input:
                    entity_name = product
                    break
        elif entity_type == 'company':
            entity_name = 'company'  # Mặc định là company
        elif entity_type == 'service':
            entity_name = 'service'  # Mặc định là service
            
        return {
            'type': entity_type,
            'name': entity_name
        } 