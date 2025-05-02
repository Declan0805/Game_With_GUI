import random

class Player:
    def __init__(self, name: str, health: int, power: int, block_chance: int, gold: int) -> None:
        self.name = name
        self.health = health
        self.power = power
        self.block_chance = block_chance
        self.gold = gold

    def attack(self) -> str:
        return f"{self.name} attacks!"

    def defend(self) -> bool:
        block = random.randint(0, 100)
        if block <= self.block_chance:
            return True
        else:
            return False

    def heal(self) -> None:
        pass

    def see_gold(self) -> int:
        return self.gold

    def print__current_stats(self) -> str:
        return f'{self.name} has {self.health} health remaining and {self.power} power with {self.gold} gold in their pockets'

    def is_alive(self) -> bool:
        return self.health > 0 