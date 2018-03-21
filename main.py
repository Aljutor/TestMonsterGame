import pandas
import numpy
from game.match.match import match
from game.monster.monster import Monster

from genetic.genetic import init_models, tournament, model_breed, evolve, create_model, fitness
from match.select import select_for_model, attack_select


if __name__ == '__main__':
    a = Monster()
    b = Monster()

    print(match(a, b))


