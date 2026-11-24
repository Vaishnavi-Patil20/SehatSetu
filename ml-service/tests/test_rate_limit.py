from app.rate_limit import SlidingWindowLimiter

def test_rate_limit_blocks_after_limit():
    limiter = SlidingWindowLimiter(limit=2, window_seconds=60)
    assert limiter.allow('user') is True
    assert limiter.allow('user') is True
    assert limiter.allow('user') is False
