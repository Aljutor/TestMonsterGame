# Stats = NamedTuple(
#     "Stats",
#     [
#         ('health',  int),
#         ('stamina', int),
#         ('damage',  int),
#         ('armor',   int),
#     ]
# )

class Stats():
    health:  int
    stamina: int
    damage:  int
    armor:   int

    def __init__(self, health: int, stamina: int, damage: int, armor: int):
        self.health  = health
        self.stamina = stamina
        self.damage  = damage
        self.armor   = armor


    def __repr__(self):
        return "health: {}, stamina: {}, damage: {}, armor: {}".format(
            self.health,
            self.stamina,
            self.damage,
            self.armor
        )


    def __iter__(self):
        return iter((
            self.health,
            self.stamina,
            self.damage,
            self.armor
        ))