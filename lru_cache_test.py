import unittest

import lru_cache


class LruCacheTest(unittest.TestCase):

  def testNumEntries(self):
    num_entries = 40
    cache = lru_cache.LruCache(num_entries=num_entries)
    for i in range(num_entries):
      cache[i] = i

    # Check that entries are bumped in the order in which they were added.
    for i in range(num_entries):
      cache[i + num_entries] = i + num_entries
      self.assertNotIn(i, cache)
      self.assertIn(i + 1, cache)

  def testLeastRecentlyUsed(self):
    # Populate the cache.
    num_entries = 40
    cache = lru_cache.LruCache(num_entries=num_entries)
    for i in range(num_entries):
      cache[i] = i

    # Accessing element 0 makes it the least-recently-used, so it should
    # persist after we add num_entries - 1 new entries.
    self.assertEqual(0, cache[0])
    for i in range(num_entries - 1):
      cache[i + num_entries] = i
    self.assertEqual(0, cache[0])

  def testKeyError(self):
    cache = lru_cache.LruCache()
    with self.assertRaises(KeyError):
      cache['foo']


if __name__ == '__main__':
  unittest.main()