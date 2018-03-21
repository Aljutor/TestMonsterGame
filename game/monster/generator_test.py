import unittest

from monster.generator import gen_stats
from monster.generator import gen_numbers

class TestStatsGenerator(unittest.TestCase):

    def test_stats_are_positive(self):
        stats = gen_stats()
        value = any(n > 0 for n in stats)
        self.assertTrue(value)

    def test_stats_count(self):
        stats = gen_stats()
        self.assertEqual(len(stats), 4)


    def test_stats_same_seed(self):
        pass


    def test_stats_same_level(self):
        pass


class TestNumGenerator(unittest.TestCase):

    def test_total_sum(self):
        total = 100
        real_total = sum(gen_numbers(10, total))
        self.assertAlmostEqual(real_total, total)

    def test_num_count(self):
        count = 10
        numbers = gen_numbers(count, 100)
        self.assertEqual(len(numbers), count)

    def test_same_seed(self):
        seed = 42
        one = gen_numbers(10, 10, seed)
        two = gen_numbers(10, 10, seed)
        self.assertEqual(one, two)



class TestScaleToRange(unittest.TestCase):
    pass


class TestScaleToLevel(unittest.TestCase):
    pass


class TestScaleStats(unittest.TestCase):
    pass


class TestNamedTuple(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()