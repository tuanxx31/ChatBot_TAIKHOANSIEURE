from datetime import datetime
from collections import deque
import time

class RateLimiter:
    def __init__(self, rpm=500, tpm=200000, reset_interval=60):
        self.request_times = deque(maxlen=rpm)
        self.token_count = 0
        self.last_token_reset = datetime.now()
        self.TOKEN_LIMIT = tpm
        self.TOKEN_RESET_INTERVAL = reset_interval

    def check(self, token_usage=0):
        now = datetime.now()
        if (now - self.last_token_reset).seconds >= self.TOKEN_RESET_INTERVAL:
            self.token_count = 0
            self.last_token_reset = now

        if len(self.request_times) >= self.request_times.maxlen:
            if (now - self.request_times[0]).seconds < 60:
                time.sleep(60 - (now - self.request_times[0]).seconds)

        if self.token_count + token_usage >= self.TOKEN_LIMIT:
            time.sleep(self.TOKEN_RESET_INTERVAL - (now - self.last_token_reset).seconds)
            self.token_count = 0
            self.last_token_reset = datetime.now()

        self.token_count += token_usage
        self.request_times.append(now)
