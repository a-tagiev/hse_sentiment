import time


class RateLimiter:
    def __init__(self, timeout: float) -> None:
        self.timeout = timeout
        self.memory = {}

    async def check(self, key: str) -> float:
        current_time = time.time()

        if key not in self.memory or current_time - self.memory[key] > self.timeout:
            self.memory[key] = current_time
            return 0

        return self.timeout - (current_time - self.memory[key])
