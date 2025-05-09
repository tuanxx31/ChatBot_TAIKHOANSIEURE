from abc import ABC, abstractmethod
from typing import List, Dict

class HotProductRepositoryInterface(ABC):
    @abstractmethod
    def get_hot_products(self) -> List[Dict]:
        """
        Lấy danh sách sản phẩm hot từ bảng top_selling_products
        """
        pass 