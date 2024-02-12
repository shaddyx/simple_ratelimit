import asyncio
import time

import pytest

from simple_ratelimit.rate_limit import RateLimit

pytest_plugins = ('pytest_asyncio',)


def test_rate_limit():
    rl = RateLimit(3, 0.1)
    start = time.time()
    rl.check(1)
    assert time.time() - start <= 0.01
    rl.check(1)
    assert time.time() - start <= 0.01
    rl.check(1)
    assert time.time() - start <= 0.01
    rl.check(1)
    assert time.time() - start >= 0.1
    #   should be cleared here
    rl.check(1)
    assert time.time() - start <= 0.11
    assert time.time() - start < 0.15

    assert len(rl.storage) != 0
    assert len(rl.time_queue) != 0

    time.sleep(0.3)
    rl.clear_old()
    assert len(rl.storage) == 0
    assert len(rl.time_queue) == 0


@pytest.mark.asyncio
async def test_async_rate_limit():
    async def delay(x):
        await asyncio.sleep(x)

    rl = RateLimit(3, 0.1)
    rl.delay_function = delay

    start = time.time()
    await rl.acheck(1)
    assert time.time() - start <= 0.01
    await rl.acheck(1)
    assert time.time() - start <= 0.01
    await rl.acheck(1)
    assert time.time() - start <= 0.01
    await rl.acheck(1)
    assert time.time() - start >= 0.1
    assert time.time() - start < 0.15
    #   should be cleared here
    await rl.acheck(1)
    assert time.time() - start <= 0.11


class Counter:
    c = 0


def test_rate_limit_spam():
    rl = RateLimit(2, 0.1)
    Counter.c = 0

    def dfunction(delay):
        print("delay executed: {}".format(delay))
        Counter.c += 1
        time.sleep(delay)
    rl.delay_function = dfunction
    for k in range(10):
        print(k)
        rl.check(1)
    assert Counter.c == 4


def test_rate_limit_spam_diff_keys():
    rl = RateLimit(2, 0.1)
    Counter.c = 0

    def dfunction(delay):
        print("delay executed: {}".format(delay))
        Counter.c += 1
        time.sleep(delay)
    rl.delay_function = dfunction
    for k in range(10):
        print(k)
        rl.check(1)
        rl.check(2)
    assert Counter.c == 9
