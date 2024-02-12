import collections
import threading
import time
import typing


class _RateLimitStorage:
    def __init__(self, key, period):
        self.key = key
        self.period = period
        self.storage = collections.deque()
        self.last_update_time = time.time()

    def clear_old(self):
        now = time.time()
        while True:
            if not self.storage:
                return
            if now - self.storage[0] > self.period:
                self.storage.popleft()
            else:
                return

    def get_for_period(self):
        self.clear_old()
        return len(self.storage)

    def append(self, timestamp):
        self.clear_old()
        self.storage.append(timestamp)


class RateLimit:

    def __init__(self, times, period, key_func: typing.Callable = lambda *args, **kwargs: 1):
        self.storage: typing.Dict[str, _RateLimitStorage] = {}
        self.time_queue = []
        self.key_func = key_func
        self.times = times
        self.period = period
        self.lock = threading.RLock()
        self.delay_function = time.sleep

    def _check_and_get(self, key):
        with self.lock:
            if key not in self.storage:
                self.storage[key] = _RateLimitStorage(key, self.period)
            return self.storage[key]

    def clear_old(self):
        with self.lock:
            now = time.time()
            while True:
                if not self.time_queue:
                    return
                if now - self.time_queue[0].last_update_time >= self.period:
                    rt_storage = self.time_queue.pop(0)
                    del self.storage[rt_storage.key]
                else:
                    return

    def _eval_storage(self, *args, **kwargs):
        with self.lock:
            k = self.key_func(*args, **kwargs)
            storage = self._check_and_get(k)
            storage.last_update_time = time.time()
            if storage in self.time_queue:
                self.time_queue.remove(storage)
            self.time_queue.append(storage)
            return storage

    def check(self, *args, **kwargs):
        storage = self._eval_storage(*args, **kwargs)
        now = time.time()
        if storage.get_for_period() >= self.times:
            self.delay_function(self.period - (now - storage.last_update_time))
        now = time.time()
        storage.last_update_time = now
        storage.append(now)

    async def acheck(self, *args, **kwargs):
        storage = self._eval_storage(*args, **kwargs)
        now = time.time()
        if storage.get_for_period() >= self.times:
            await self.delay_function(self.period - (now - storage.last_update_time))
        now = time.time()
        storage.last_update_time = now
        storage.append(now)
