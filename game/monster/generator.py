import math
import random

from typing import List
from typing import Tuple

from .stats import Stats

def gen_numbers(count: int, points: int, seed: int = None) -> List[float]:
    if count < 1:
        raise Exception

    if points < 1:
        raise Exception

    random.seed(seed)

    numbers = [random.randrange(1, 101) for _ in range(0, count)]
    total = sum(numbers)
    numbers = [((n / total) * points) for n in numbers]

    return numbers


def scale_to_range(number: int, old_range: Tuple[int, int], new_range: Tuple[int, int]) -> int:
    old_min, old_max = old_range
    new_min, new_max = new_range

    result = (((new_max - new_min) * (number - old_min)) / (old_max - old_min)) + new_min
    return int(math.ceil(result))


def scale_to_level(number: int, level: int) -> int:
    if level < 1:
        raise Exception

    result = number * (level ** (3 / 2))

    return int(math.ceil(result))


def scale_stats(stats: Stats, level) -> Stats:
    if level < 1:
        raise Exception

    health, stamina, damage, armor = stats

    health  = scale_to_level(health, level)
    stamina = scale_to_range(stamina, (1, 24), (3, 12))
    damage  = scale_to_level(damage, level)
    armor   = scale_to_level(armor, level)

    return Stats(health, stamina, damage, armor)


def gen_stats(seed: int = None, level: int = 1) -> Stats:
    # Totally magic generator
    # Goal - generate stats for a beast depends on it's level

    # Points system - max total points is 24 for all stats
    # We select 4 random numbers with total sum = 24

    if level < 1:
        raise Exception('Argument level less 1')

    total_points: int = 24

    numbers = gen_numbers(4, total_points, seed=seed)
    stats = Stats(*numbers)

    stats = scale_stats(stats, level)
    return stats
