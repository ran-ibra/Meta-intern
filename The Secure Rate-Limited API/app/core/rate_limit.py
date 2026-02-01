import time
from collections import defaultdict, deque
from fastapi import HTTPException, status
from app.core.config import settings

# key -> deque[timestamps]
_BUCKETS: dict[str, deque] = defaultdict(deque)

def check_rate_limit(key: str):
    now = time.time()
    window = 60
    limit = settings.RATE_LIMIT_PER_MINUTE

    q = _BUCKETS[key]
    # remove old timestamps
    while q and (now - q[0]) > window:
        q.popleft()

    if len(q) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {limit} requests per minute"
        )

    q.append(now)
