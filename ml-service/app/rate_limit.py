from collections import defaultdict, deque
from time import monotonic

class SlidingWindowLimiter:
    def __init__(self, limit: int = 30, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.events = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = monotonic(); q = self.events[key]
        while q and now - q[0] >= self.window_seconds: q.popleft()
        if len(q) >= self.limit: return False
        q.append(now); return True
