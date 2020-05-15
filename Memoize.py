import functools


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, unless returned value is equal to None
   """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            if value is not None:
                self.cache[args] = value
            return value

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
