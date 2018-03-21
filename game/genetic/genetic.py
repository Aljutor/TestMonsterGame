import tensorflow as tf

import itertools
from keras.models import Sequential
from keras.layers import Dense

from game.match.select import select_for_model, attack_select
from game.match.match import match

from game.monster.monster import Monster

def create_model():
    model = Sequential()
    model.add(Dense(64, input_dim=8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def init_models(count: int, x_train, y_train):
    pool = []

    for i in range(count):
        model = create_model()
        model.fit(x_train, y_train, epochs=1)
        model.set_weights(weights_mutate(model.get_weights()))

        pool.append(model)

    return pool


def weights_crossover(weights_a, weights_b):

    weights_new_a = weights_a.copy()
    weights_new_b = weights_b.copy()

    weights_new_a[0] = weights_b[0]
    weights_new_b[0] = weights_a[0]


    return [weights_new_a, weights_new_b]

import random

def weights_mutate(weights):
    random.seed()
    for xi in range(len(weights)):
        for yi in range(len(weights[xi])):
            if random.uniform(0, 1) > 0.85:
                change = random.uniform(-0.5, 0.5)
                weights[xi][yi] += change

    return weights


def model_breed(model_a, model_b):
    new_weights = weights_crossover(model_a.get_weights(), model_b.get_weights())

    new_weights_a = weights_mutate(new_weights[0])
    new_weights_b = weights_mutate(new_weights[1])

    new_model_a = create_model()
    new_model_a.set_weights(new_weights_a)

    new_model_b = create_model()
    new_model_b.set_weights(new_weights_b)

    return [new_model_a, new_model_b]


def tournament(models):

    data = [{'model': model, 'wins': 0} for model in models]

    for a, b in itertools.combinations(data, 2):
        select_a = select_for_model(a['model'])
        select_b = select_for_model(b['model'])

        for _ in range(10):
            monster_a = Monster(level=1)
            monster_b = Monster(level=1)

            result, log = match(monster_a, monster_b, select_a, select_b)

            if result is result.WinA:
                a['wins'] += 1

            if result is result.WinB:
                b['wins'] += 1

    return sorted(data, key=lambda x: x['wins'], reverse=True)



def tournament2(models):
    # data = [{'model': model, 'wins': 0} for model in models]

    fitnesses = map(fitness, models)

    data = [ {'model': m, 'wins': f} for m, f in zip(models, fitnesses)]

    return sorted(data, key=lambda x: x['wins'], reverse=True)



def fitness(model) -> int:
    select_a = select_for_model(model)
    total_fitness = 0

    for _ in range(1000):
        monster_a = Monster(level=1)
        monster_b = Monster(level=1)

        result, log = match(monster_a, monster_b, select_a, attack_select)

        if result is result.WinA:
            total_fitness += 1

    return total_fitness

def evolve(generations :int, x_train, y_train):
    models = init_models(10, x_train, y_train)


    for gen in range(generations):
        result = tournament2(models)
        print('Generation: ',gen)
        print('Fitness: ', result[0]['wins'])

        new_models = model_breed(result[0]['model'], result[1]['model'])
        mutant = create_model()
        mutant.set_weights(weights_mutate(result[0]['model'].get_weights()))

        models = new_models + [mutant] + [r['model'] for r in result[:-3]]

    result = tournament(models)
    print('final')
    print(result[0])
    print(result[1])

    return result