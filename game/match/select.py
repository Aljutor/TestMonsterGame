import random
import numpy

from typing import Callable
from typing import NewType

from game.monster.monster import Monster

from .move import Move

SelectFunc = NewType('SelectFunc', Callable[[Monster, Monster], Move])

def random_select(m: Monster, e: Monster) -> Move:
    random.seed()
    move = random.choice(list(Move))

    return move

def attack_select(m: Monster, e: Monster) -> Move:
    return Move.Attack

def block_select(m: Monster, e: Monster) -> Move:
    return Move.Block


def select_for_model(model) -> SelectFunc:
    def select(m: Monster, e: Monster) -> Move:
        input = numpy.array([list(m.cur_stats) + list(e.cur_stats)])

        result = model.predict_classes(input)
        result = result[0][0]

        return Move(result)

    return select

