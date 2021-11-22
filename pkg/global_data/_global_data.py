import threading

_cache = dict()
_lock = threading.Lock()
_lock_val = 1


def get(key):
    return _cache[key]


def put(key, value):
    _lock.acquire(_lock_val)
    _cache[key] = value
    _lock.release()


def delete(key):
    _lock.acquire(_lock_val)
    _cache.pop(key)
    _lock.release()
