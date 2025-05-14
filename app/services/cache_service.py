from datetime import datetime, timedelta
from typing import Dict

class CacheService:
    def __init__(self, duration_hours=24):
        self.cache: Dict[str, str] = {}
        self.expiry: Dict[str, datetime] = {}
        self.duration = timedelta(hours=duration_hours)

    def is_valid(self, key: str) -> bool:
        return key in self.expiry and datetime.now() < self.expiry[key]

    def get(self, key: str) -> str:
        return self.cache.get(key, "")

    def set(self, key: str, value: str):
        self.cache[key] = value
        self.expiry[key] = datetime.now() + self.duration

    def clear(self):
        self.cache.clear()
        self.expiry.clear()
