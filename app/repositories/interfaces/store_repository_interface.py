from abc import ABC, abstractmethod
from typing import Optional, Dict

class StoreRepositoryInterface(ABC):
    @abstractmethod
    def get_store_config(self) -> Optional[Dict]:
        """
        Lấy thông tin cửa hàng từ bảng configs
        """
        pass 