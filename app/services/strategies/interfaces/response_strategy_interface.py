from abc import ABC, abstractmethod
from typing import Dict, Tuple

class ResponseStrategyInterface(ABC):
    @abstractmethod
    def format_response(self, user_input: str, analysis: Dict, raw_data: Dict) -> Tuple[str, str]:
        """
        Định dạng câu trả lời
        Returns:
            Tuple[str, str]: (user_prompt, system_prompt)
        """
        pass 