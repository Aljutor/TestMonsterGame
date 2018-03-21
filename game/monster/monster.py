
from monster.stats import Stats
from monster.generator import gen_stats


class Monster:
    level: int

    cur_stats: Stats
    max_stats: Stats


    def __init__(self, level: int = 1, seed: int = None) -> None:
        super ().__init__ ()

        self.level = level

        self.max_stats = gen_stats(seed, level)
        self.cur_stats = self.max_stats


    def __repr__(self) -> str:
        return 'Monster({})'.format(self.cur_stats)


    # TODO Refactor this methods
    def minus_health(self, count: int):
        self.cur_stats.health -= count

        if self.cur_stats.health < 0:
            self.cur_stats.health = 0

    def plus_health(self, count: int):
        self.cur_stats.health += count

        if self.cur_stats.health > self.max_stats.health:
            self.cur_stats.health = self.max_stats.health

    def minus_stamina(self, count: int):
        self.cur_stats.stamina -= count

        if self.cur_stats.stamina < 0:
            self.cur_stats.stamina = 0

    def plus_stamina(self, count: int):
        self.cur_stats.stamina += count

        if self.cur_stats.stamina > self.max_stats.stamina:
            self.cur_stats.stamina = self.max_stats.stamina

    @property
    def is_alive(self) -> bool:
        if self.cur_stats.health > 0:
            return True

        return False

    def check_stamina(self, count: int) -> bool:
        if self.cur_stats.stamina >= count:
            return True

        return False

    def attack(self) -> int:
        if not self.is_alive:
            return 0

        if not self.check_stamina(3):
            return 0

        self.minus_stamina(3)
        return self.cur_stats.damage

    def block(self, damage: int):
        if not self.is_alive:
            return

        if not self.check_stamina(2):
            self.minus_health(damage)

        if damage < 1:
            self.minus_stamina(2)
            return

        last = damage - self.cur_stats.armor
        if last < 0:
            last = 1

        self.minus_health(last)
        self.minus_stamina(2)

    def update(self):
        self.plus_stamina(1)
