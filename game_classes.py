import random


class Player:
    def __init__(self, name, health, power, block_chance, gold):
        self.name = name
        self.health = health
        self.power = power
        self.block_chance = block_chance
        self.gold = gold

    def attack(self):
        return f"{self.name} attacks!"

    def defend(self):
        block = random.randint(0, 100)
        if block <= self.block_chance:
            return True
        else:
            return False

    def heal(self):
        pass

    def see_gold(self):
        return self.gold

    def print__current_stats(self):
        return f'{self.name} has {self.health} health remaining and {self.power} power with {self.gold} gold in their pockets'

    def is_alive(self):
        return self.health > 0


class Enemy(Player):
    def __init__(self, name, health, power, block_chance, reward_gold):
        super().__init__(name, health, power, 25, 0)
        self.reward_gold = reward_gold

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f'Enemy name: {self.name}, health: {self.health}, Gold reward for defeating the enemy: {self.reward_gold}'






