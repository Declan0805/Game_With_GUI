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

    def can_afford_action(self, action: dict) -> bool:
        """
        Checks if the player can afford an action based on its gold cost.
        
        Takes in the actions from the dictionary to find the results that require money (i.e. Parley):
            action (dict): The action dictionary containing success/failure outcomes
            
        Returns:
            bool: True if the player can afford the action, False otherwise
        """
        # Check success case gold cost
        success_cost = action.get("success", {}).get("gold", 0)
        if success_cost < 0 and abs(success_cost) > self.gold:
            return False
            
        # Check failure case gold cost
        failure_cost = action.get("failure", {}).get("gold", 0)
        if failure_cost < 0 and abs(failure_cost) > self.gold:
            return False
            
        return True 