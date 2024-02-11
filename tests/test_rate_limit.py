import asyncio
import time

import pytest

from simple_ratelimit.rate_limit import RateLimit

pytest_plugins = ('pytest_asyncio',)


def test_rate_limit():
    rl = RateLimit(3, 1)
    start = time.time()
    rl.check(1)
    assert time.time() - start <= 0.1
    rl.check(1)
    assert time.time() - start <= 0.1
    rl.check(1)
    assert time.time() - start <= 0.1
    rl.check(1)
    assert time.time() - start >= 1
    #   should be cleared here
    rl.check(1)
    assert time.time() - start <= 1.1

    assert len(rl.storage) != 0
    assert len(rl.time_queue) != 0

    time.sleep(3)
    rl.clear_old()
    assert len(rl.storage) == 0
    assert len(rl.time_queue) == 0


@pytest.mark.asyncio
async def test_async_rate_limit():
    async def delay(x):
        await asyncio.sleep(x)
    rl = RateLimit(3, 1)
    rl.delay_function = delay

    start = time.time()
    await rl.acheck(1)
    assert time.time() - start <= 0.1
    await rl.acheck(1)
    assert time.time() - start <= 0.1
    await rl.acheck(1)
    assert time.time() - start <= 0.1
    await rl.acheck(1)
    assert time.time() - start >= 1
    #   should be cleared here
    await rl.acheck(1)
    assert time.time() - start <= 1.1
