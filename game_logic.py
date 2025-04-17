from game_classes import Player, Enemy
import random



class Item:
    def __init__(self, name, key, equipment_type=None):
        self.name = name
        self.key = key
        self.equipment_type = equipment_type

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def random_scenarios(player):
    """
    Returns a random scenario with weighted probabilities.
    """
    scenarios = {
        1: {
            "description": "You encounter a group of goblins ambushing the road ahead!",
            "results": {
                "fight": {
                    "enemy": {"name": "Goblin", "health": 100, "power": 10, "reward_gold": 50},
                    "success": {"description": "You defeated the goblins and looted gold!", "health": 0, "gold": 50},
                    "failure": {"description": "The goblins overwhelmed you, and you fled injured.", "health": -20,
                                "gold": 0},
                    "chance": 70
                },
                "run": {
                    "success": {"description": "You escaped safely, avoiding conflict.", "health": 0, "gold": 0},
                    "failure": {"description": "You tripped while running and got injured!", "health": -10, "gold": 0},
                    "chance": 90
                },
                "parley": {
                    "success": {"description": "You bribed the goblins, and they let you go.", "health": 0,
                                "gold": -20},
                    "failure": {"description": "The goblins took your gold and still attacked!", "health": -15,
                                "gold": -20},
                    "chance": 60
                }
            }
        },
        2: {
            "description": "You find a locked treasure chest in an abandoned loot pile.",
            "results": {
                "open": {
                    "success": {"description": "You unlocked it and found precious gems!", "health": 0, "gold": 100},
                    "failure": {"description": "The chest was trapped. You got injured!", "health": -15, "gold": 0},
                    "chance": 50
                },
                "ignore": {
                    "success": {"description": "You wisely avoided the chest—sometimes caution pays off.", "health": 0,
                                "gold": 0},
                    "failure": {"description": "You left behind what could have been treasure.", "health": 0,
                                "gold": 0},
                    "chance": 100
                },
                "smash": {
                    "success": {"description": "You smashed the chest open and grabbed the loot!", "health": 0,
                                "gold": 75},
                    "failure": {"description": "The chest exploded! It was trapped.", "health": -10, "gold": 0},
                    "chance": 60
                }
            }
        },
        4: {  # Rest scenario
            "description": "You find a quiet spot to rest and gather your thoughts.",
            "results": {
                "heal": {
                    "success": {"description": "You recover some health during your rest.", "health": 20, "gold": 0},
                    "failure": {"description": "You couldn’t rest properly due to nearby noises.", "health": 0,
                                "gold": 0},
                    "chance": 100
                },
                "Leave": {
                    "success": {"description": "You leave the potential campsite.",
                                "health": 15, "gold": 0},
                    "failure": {"description": "NaN",
                                "health": 0, "gold": 0},
                    "chance": 100
                }
            }
        }
    }


    scenario_keys = list(scenarios.keys())
    selected_key = random.choices(scenario_keys)[0]

    return scenarios[selected_key]



def resolve_action(player, action):
    """
    Resolves the outcome of a player's action.

    Takes in the player object and the action dictionary.

    Then it returns the action dictionary and any changes to the player's health and gold.'
    """
    roll = random.randint(1, 100)
    if roll <= action["chance"]:  # Success
        result = action["success"]
        player.health += result["health"]
        player.gold += result["gold"]
        return {"result": "success", "description": result["description"]}
    else:  # Failure
        result = action["failure"]
        player.health += result["health"]
        player.gold += result["gold"]
        return {"result": "failure", "description": result["description"]}


def handle_combat(player, enemy_data):
    """
    Handles combat scenarios and determines the outcome based on random int generation
    Returns a dictionary with the combat outcome and combat log.
    The combat log is a list of strings representing the combat events and their results
    """
    enemy = Enemy(
        name=enemy_data["name"],
        health=enemy_data["health"],
        power=enemy_data["power"],
        block_chance=enemy_data.get("block_chance", 25),
        reward_gold=enemy_data["reward_gold"]
    )

    combat_log = []

    while enemy.is_alive() and player.is_alive():
        # Player attack
        win_chance = random.randint(1, 100)
        if win_chance > enemy.block_chance:
            damage = player.power
            enemy.health -= damage
            combat_log.append(f"You dealt {damage} damage to the {enemy.name}. Remaining health: {enemy.health}")
        else:
            combat_log.append(f"The {enemy.name} blocked your attack!")

        # Enemy attack
        enemy_win_chance = random.randint(1, 100)
        if enemy_win_chance > player.block_chance:
            player.health -= enemy.power
            combat_log.append(f"{enemy.name} attacked you for {enemy.power} damage. Your health: {player.health}")
        else:
            combat_log.append(f"You blocked the {enemy.name} attack.")

        if not player.is_alive():
            combat_log.append("Fatal Blow")
            return {"status": "defeat", "combat_log": combat_log}

    # Victory logic
    if not enemy.is_alive():
        player.gold += enemy.reward_gold

        combat_log.append(f"You defeated the {enemy.name} and gained {enemy.reward_gold} gold!")
        return {"status": "victory", "combat_log": combat_log}

    return {"status": "ongoing", "combat_log": combat_log}



if __name__ == "__main__":
    # For standalone testing purposes
    player = Player("Hero", 100, 25, 20, 0)


    while player.is_alive():
        scenario = random_scenarios(player)
        print(f"\nScenario: {scenario['description']}")
        print("Options:", ", ".join(scenario["results"].keys()))
        action_choice = input("Choose your action: ").strip().lower()

        if action_choice in scenario["results"]:
            action = scenario["results"][action_choice]
            if "enemy" in action:
                combat = handle_combat(player, action["enemy"])
                print("\n".join(combat["combat_log"]))
                if combat["status"] == "defeat":
                    break
            else:
                outcome = resolve_action(player, action)
                print(outcome["description"])
        else:
            print("Invalid choice. Try again.")
