from player import Player

class Enemy(Player):
    def __init__(self, name: str, health: int, power: int, block_chance: int, reward_gold: int) -> None:
        super().__init__(name, health, power, 25, 0)
        self.reward_gold = reward_gold

    def is_alive(self) -> bool:
        return self.health > 0

    def __str__(self) -> str:
        return f'Enemy name: {self.name}, health: {self.health}, Gold reward for defeating the enemy: {self.reward_gold}' 