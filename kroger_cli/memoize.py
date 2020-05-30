import functools
import pickle
from datetime import datetime, timedelta


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, unless returned value is equal to None
    """

    cache_file = '.cache.pkl'
    cache_expiration_hours = 1
    default_cache = {
        'expire': datetime.now() + timedelta(hours=cache_expiration_hours),
        'data': {}
    }

    def __init__(self, func):
        self.func = func
        self.cache = self.default_cache
        self._init_file_cache()

    def __call__(self, *args):
        key = self.func.__name__
        if key in self.cache['data']:
            return self.cache['data'][key]
        else:
            value = self.func(*args)
            if value is not None:
                self.cache['data'][key] = value
                self._save_cache_file()
            return value

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

    def _init_file_cache(self):
        try:
            with open(self.cache_file, 'rb') as f:
                cache = pickle.load(f)
        except Exception:
            cache = None

        if cache is not None:
            self.cache = cache

        if 'expire' in self.cache and datetime.now() > self.cache['expire']:
            self.cache = self.default_cache

    def _save_cache_file(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f, pickle.HIGHEST_PROTOCOL)
