from enum import IntEnum
from typing import List

from game.monster.monster import Monster

from .move import Move
from .select import SelectFunc
from .select import random_select


def update(a :Monster, b: Monster, select_a :SelectFunc, select_b: SelectFunc):

    a.update()
    b.update()

    # print ('a:', a)
    # print ('b:', b)

    move_a = select_a(a, b)
    move_b = select_b(b, a)

    log = [int(move_a), int(move_b)] + list(a.cur_stats) + list(b.cur_stats)

    if move_a == Move.Attack and move_b == Move.Attack:
        a.minus_health(b.attack())
        b.minus_health(a.attack())

    if move_a == Move.Attack and move_b == Move.Block:
        b.block(a.attack())

    if move_a == Move.Block  and move_b == Move.Attack:
        a.block(b.attack())

    if move_a == Move.Block  and move_b == Move.Block:
        a.block(0)
        b.block(0)

    # print('move_a:', move_a, 'move_b', move_b)
    # print('a:', a)
    # print('b:', b)
    # print()

    return log

class MatchResult(IntEnum):
    Draw  =  -1
    WinA  =   0
    WinB  =   1

def match(a: Monster, b: Monster, select_a :SelectFunc = None, select_b: SelectFunc = None) -> (MatchResult, List):
    updates_count = 0

    logs = []

    if select_a is None:
        select_a = random_select

    if select_b is None:
        select_b = random_select

    while a.is_alive and b.is_alive and updates_count < 10:
        logs.append(update(a, b, select_a, select_b))
        updates_count += 1

    if (a.is_alive) and (b.is_alive):
        return MatchResult.Draw, logs

    if (not a.is_alive) and (not b.is_alive):
        return MatchResult.Draw, logs

    if (a.is_alive):
        return MatchResult.WinA, logs

    if (b.is_alive):
        return MatchResult.WinB, logs