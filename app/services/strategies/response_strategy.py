from abc import ABC, abstractmethod
import json

class ResponseStrategy(ABC):
    @abstractmethod
    def format_response(self, user_input: str, analysis: dict, raw_data: dict) -> str:
        pass

class CTVResponseStrategy(ResponseStrategy):
    def format_response(self, user_input: str, analysis: dict, raw_data: dict) -> str:
        if not raw_data:
            return "Xin lỗi, tôi không tìm thấy thông tin về sản phẩm này."

        system_prompt = """Bạn là nhân viên tư vấn cho CTV. Trả lời tự nhiên, thân thiện bằng tiếng Việt.
        Khi đề cập đến giá, luôn sử dụng giá gốc (price) thay vì giá khuyến mãi.
        Trình bày rõ ràng, thêm thông tin hữu ích và sẵn sàng hỗ trợ thêm."""

        product_info = {
            "tên": raw_data['name'],
            "mô_tả": raw_data['description'],
            "gói_cước": self._format_packages(raw_data['product_package'])
        }

        user_prompt = f"Khách hỏi: {user_input}\nThông tin: {json.dumps(product_info, ensure_ascii=False)}"
        return user_prompt, system_prompt

    def _format_packages(self, packages):
        formatted_packages = []
        for pkg in packages:
            formatted_pkg = {
                "tên": pkg['name'],
                "giá": pkg['price'],
                "trạng_thái": "Còn hàng" if pkg.get('stock', True) else "Hết hàng"
            }
            formatted_packages.append(formatted_pkg)
        return formatted_packages

class UserResponseStrategy(ResponseStrategy):
    def format_response(self, user_input: str, analysis: dict, raw_data: dict) -> str:
        if not raw_data:
            return "Xin lỗi, tôi không tìm thấy thông tin về sản phẩm này."

        system_prompt = """Bạn là nhân viên tư vấn cho khách hàng. Trả lời tự nhiên, thân thiện bằng tiếng Việt.
        Khi đề cập đến giá, luôn sử dụng giá khuyến mãi (discountPrice) thay vì giá gốc.
        Trình bày rõ ràng, thêm thông tin hữu ích và sẵn sàng hỗ trợ thêm."""

        product_info = {
            "tên": raw_data['name'],
            "mô_tả": raw_data['description'],
            "gói_cước": self._format_packages(raw_data['product_package'])
        }

        user_prompt = f"Khách hỏi: {user_input}\nThông tin: {json.dumps(product_info, ensure_ascii=False)}"
        return user_prompt, system_prompt

    def _format_packages(self, packages):
        formatted_packages = []
        for pkg in packages:
            formatted_pkg = {
                "tên": pkg['name'],
                "giá": pkg['discountPrice'],
                "trạng_thái": "Còn hàng" if pkg.get('stock', True) else "Hết hàng"
            }
            formatted_packages.append(formatted_pkg)
        return formatted_packages 