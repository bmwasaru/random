import collections


class LruCache(object):

    _DEFAULT_NUM_OF_ENTRIES = 200

    def __init__(self, num_entries=None):
        self._num_entries = (self._DEFAULT_NUM_OF_ENTRIES if num_entries is None else num_entries)
        self._cache = collections.OrderedDict()

    def __getitem__(self, key):
        if key not in self._cache:
            raise KeyError(key)

        value = self._cache.pop(key)
        self._cache[key] = value

        return value

    def __setitem__(self, key, value):
        if len(self._cache) == self._num_entries:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def __contains__(self, key):
        return key in self._cache
