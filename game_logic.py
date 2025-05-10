from player import Player
from enemy import Enemy
import random



def random_scenarios(player: Player) -> dict:
    """
    Provides a random scenario from a predefined dictionary of possible scenarios

    Each scenario contains a description and potential outcomes based on the player's choices,
    such as actions they can take.
    Each action may lead to success or failure, which impacts the player's health or gold.
    The success of these outcomes is determined using the random.choice method.
    Returns a dictionary representing the selected scenario.
    The scenario contains a description and possible-
    results (actions and outcomes), including success and failure outcomes for each action.
    """
    scenarios = {
        1: {
            "description": "You encounter a group of goblins ambushing the road ahead!",
            "results": {
                "Fight": {
                    "enemy": {"name": "Goblin", "health": 100, "power": 10, "reward_gold": 50},
                    "success": {"description": "You defeated the goblins and looted gold!", "health": 0, "gold": 50},
                    "failure": {"description": "The goblins overwhelmed you, and you fled injured.", "health": -20,
                                "gold": 0},
                    "chance": 70
                },
                "Run": {
                    "success": {"description": "You escaped safely, avoiding conflict.", "health": 0, "gold": 0},
                    "failure": {"description": "You tripped while running and got injured!", "health": -10, "gold": 0},
                    "chance": 85
                },
                "Parley": {
                    "success": {"description": "You bribed the goblins, and they let you go.", "health": 0,
                                "gold": -20},
                    "failure": {"description": "The goblins took your gold and still attacked!", "health": -15,
                                "gold": -20},
                    "chance": 50
                }
            }
        },
        2: {
            "description": "You find a locked treasure chest in an abandoned loot pile.",
            "results": {
                "Open": {
                    "success": {"description": "You unlocked it and found precious gems!", "health": 0, "gold": 100},
                    "failure": {"description": "The chest was trapped. You got injured!", "health": -15, "gold": 0},
                    "chance": 60
                },
                "Ignore": {
                    "success": {"description": "You wisely avoided the chest—sometimes caution pays off.", "health": 0,
                                "gold": 0},
                    "failure": {"description": "You left behind what could have been treasure.", "health": 0,
                                "gold": 0},
                    "chance": 50
                },
                "Smash": {
                    "success": {"description": "You smashed the chest open and grabbed the loot!\nHowever some of the loot was broken when you smashed it open", "health": 0,
                                "gold": 75},
                    "failure": {"description": "The chest exploded! It was trapped.", "health": -10, "gold": 0},
                    "chance": 50
                }
            }
        },
        4: {  # Rest scenario
            "description": "You find a quiet spot to rest and gather your thoughts.",
            "results": {
                "Heal": {
                    "success": {"description": "You recover some health during your rest.", "health": 20, "gold": 0},
                    "failure": {"description": "You couldn't rest properly due to nearby noises.", "health": 0,
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
        },
        5: {
            "description": "You encounter a massive dragon blocking the road ahead!\n(Recommended Health:300, Recommended Power: 80",
            "results": {
                "Fight": {
                    "enemy": {"name": "Dragon", "health": 500, "power": 30,"block_chance": 30, "reward_gold": 50},
                    "success": {"description": "You defeated the Dragon and looted gold!", "health": 0, "gold": 50},
                    "failure": {"description": "The Dragon overwhelmed you, and you fled injured.", "health": -20,
                                "gold": 0},
                    "chance": 70
                },
                "Run": {
                    "success": {"description": "You escaped safely, avoiding conflict.", "health": 0, "gold": 0},
                    "failure": {"description": "You tripped while running and got injured!", "health": -10, "gold": 0},
                    "chance": 80
                },
                "Parley": {
                    "success": {"description": "You bribed the goblins, and they let you go.", "health": 0,
                                "gold": -20},
                    "failure": {"description": "The goblins took your gold and still attacked!", "health": -15,
                                "gold": -20},
                    "chance": 50
                }
            }
        },
        6: {  # Rest scenario
            "description": "You find a wandering merchant who appears to be selling potions",
            "results": {
                "Purchase": {
                    "success": {"description": "The potion heals you", "health": 20, "gold": -10},
                    "failure": {"description": "The potion makes you sick", "health": -10,
                                "gold": -10},
                    "chance": 50
                },
                "Rob": {
                    "success": {"description": "You successfully rob the merchant and take his gold and a potion.",
                                "health": 10, "gold": 25},
                    "failure": {"description": "You attempt to rob the merchant but it goes wrong. He stabs you in the arm as you attempt to pickpocket him.",
                                "health": -20, "gold": 0},
                    "chance": 10
                },
                "Leave": {
                    "success": {"description": "You leave the merchant behind.",
                                "health": 0, "gold": 0},
                    "failure": {"description": "NaN", "health": 0, "gold": 0},
                    "chance": 100
                }
            }
        },
        7: {  # Rest scenario
            "description": "You find a pile of gold, see if you can get it.",
            "results": {
                "Grab": {
                    "success": {"description": "You get the gold.", "health": 0, "gold": 1000},
                    "failure": {"description": "The gold vanishes.", "health": 0,
                                "gold": 0},
                    "chance": random.randint(1,100)
                },
                "Swipe": {
                    "success": {"description": "You get the gold.",
                                "health": 0, "gold": 1000},
                    "failure": {"description": "The gold vanishes.",
                                "health": 0, "gold": 0},
                    "chance": random.randint(10,50)
                },
                "Steal": {
                    "success": {"description": "You get the gold.",
                                "health": 0, "gold": 1000},
                    "failure": {"description": "The gold vanishes.", "health": 0, "gold": 0},
                    "chance": random.randint(1,10)
                }
            }
        },
        8: {
            "description": "You have a chance here to spend all your gold and get a blessing granting you 1000 health or lose all your health.",
            "results": {
                "Offer to the Shrine": {
                    "success": {"description": "You are blessed.", "health": 1000, "gold": -player.gold if player.gold > 0 else -10},
                    "failure": {"description": "Lightning bolts come down from the sky and strike you down.", "health": -1000000000000000000000000,
                                "gold": -player.gold if player.gold > 0 else -10},
                    "chance": random.randint(1,100)
                },
                "Leave": {"success": {"description": "You leave the campsite.", "health": 0, "gold": 0},
                          "failure": {"description": "NaN", "health": 0, "gold": 0}, "chance": 100},
                            "chance": 100
            }
        }
    }

    scenario_keys = list(scenarios.keys())
    selected_key = random.choices(scenario_keys)[0]

    return scenarios[selected_key]



def resolve_action(player, action) -> dict:
    """
    Resolves the outcome of a player's action.

    Takes in the player object and the action dictionary.

    Then it returns the action dictionary and any changes to the player's health and gold.
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


def handle_combat(player, enemy_data) -> dict:
    """
    Handles a turn-based combat sequence between a player and an enemy.

    The combat system alternates between the player and the enemy attacking
    each other, taking into account block chances for both sides. The combat
    ends in either victory or defeat depending on the health of the combatants.
    Victory rewards the player with gold, while defeat ends the game. A combat
    log is maintained to describe all actions and outcomes during the fight. The log is used
    by the GUI to display the combat history for the scenario, provides some immersion



    Returns a dictionary containing the combat status and the combat log.
        The keys include:
            - status (str): Indicates the final combat state, which may be
             'victory', 'defeat', or 'ongoing'.

            - combat_log (list): A list of strings detailing each combat event including attacks,
            blocks, and final outcomes.
    """

    # Creates object from the enemy data listed in the scenario.
    enemy = Enemy(
        name=enemy_data["name"],
        health=enemy_data["health"],
        power=enemy_data["power"],
        block_chance=enemy_data.get("block_chance", 25), # If no block_chance is implemented it defaults to 25
        reward_gold=enemy_data["reward_gold"]
    )

    combat_log = []

    while enemy.is_alive() and player.is_alive():
        # Player attack, checks if blocked
        win_chance = random.randint(1, 100)
        if win_chance > enemy.block_chance:
            damage = player.power
            enemy.health -= damage
            combat_log.append(f"You dealt {damage} damage to the {enemy.name}. Remaining health: {enemy.health}")
        else:
            combat_log.append(f"The {enemy.name} blocked your attack!")

        # Enemy attack, also checks if blocked
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
    # For standalone testing purposes, needs redone to be useful due to affordability checking that wasn't implemented into this portion
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
