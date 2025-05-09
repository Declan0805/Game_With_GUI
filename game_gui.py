import tkinter as tk
from tkinter import ttk, messagebox
import csv
import game_logic
from player import Player
from game_logic import handle_combat, random_scenarios


"""
All buttons and general window information came from me
(Except for dynamic buttons)
The aesthetic elements were sourced partly but not entirely by an AI source
Errors in SaveGame and LoadGame logic were partly aided but AI but AI got a decent amount of it wrong so I did most of the work in the end
All Scenario information was done by me unless any major errors occurred in the code that I couldn't weed through
This was the 5th attempt so there was a ton of copy and pasting and major editing to be done from previous versions
This was the first version to be uploaded to github once I decided it was the proper direction
I separated as much logic as I could into gamelogic but while I was in this file I had already,
began work on the savegame and loadgame logic so I just continued here because I was frustrated and wanted it to just work

"""
class GameGUI:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Game GUI")
        # My work
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        # AI sourced
        self.player = Player("Hero", health=100, power=20, block_chance=25, gold=0)
        self.enemy = None
        # My Work
        self.create_widgets()
        self.scenario_counter = 0
        self.start_new_scenario()

    def create_widgets(self) -> None:
        # AI Sourced
        self.stats_frame = ttk.LabelFrame(self.root, text="Player Stats", padding=10)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # My work
        self.health_label = ttk.Label(self.stats_frame, text=f"Health: {self.player.health}")
        self.health_label.pack(anchor="w")
        # My work
        self.power_label = ttk.Label(self.stats_frame, text=f"Power: {self.player.power}")
        self.power_label.pack(anchor="w")
        self.block_chance_label = ttk.Label(self.stats_frame, text=f"Block Chance: {self.player.block_chance}")
        self.block_chance_label.pack(anchor="w")
        # My work
        self.gold_label = ttk.Label(self.stats_frame, text=f"Gold: {self.player.gold}")
        self.gold_label.pack(anchor="w")

        # Scenario description frame - AI Sources
        self.scenario_frame = ttk.LabelFrame(self.root, text="Scenario", padding=10)
        self.scenario_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        # Text - My work
        self.scenario_text = tk.Text(self.scenario_frame, width=50, height=10, wrap=tk.WORD, state="disabled")
        self.scenario_text.pack()

        # Action buttons - AI sources
        self.actions_frame = ttk.Frame(self.root)
        self.actions_frame.grid(row=1, column=0, columnspan=3, pady=20)
        """
        The below dynamic typing system works by creating a list of buttons 
        and then dynamically adding them to the frame
        It starts with an initializing an empty named list called actions
        Then it loops through a range of numbers from 0 to 3 
        (Can Be changed to higher if anybody ever adds more actions)
        Inside the loop it creates a button with the text Action 1, Action 2, etc.
        It then adds the button to the actions list and then adds it to the frame
        Later on the text inside the button changes to whatever the appropriate action is
        This is just an initialization system for the later scenarios to change the precreated button
        """
        self.actions = []
        for i in range(3):  # Create up to 3 action buttons dynamically - Done by AI
            btn = ttk.Button(self.actions_frame, text=f"Action {i + 1}",
                             command=lambda idx=i: self.handle_action_ui(idx))
            btn.grid(row=1, column=i, padx=10)
            self.actions.append(btn)


        quit_button = ttk.Button(self.actions_frame, text="Quit", command=self.quit_game)
        quit_button.grid(row=2, column=0, padx=10, pady=20)
        save_button = ttk.Button(self.actions_frame, text="Save", command=self.save_game)
        save_button.grid(row=2, column=1, padx=10, pady=20)
        load_button = ttk.Button(self.actions_frame, text="Load", command=self.load_game)
        load_button.grid(row=2, column=2, padx=10, pady=20)

        # Add continue button
        self.continue_button = ttk.Button(self.actions_frame, text="Continue", command=self.continue_to_next_scenario, state=tk.DISABLED)
        self.continue_button.grid(row=0, column=1, padx=10, pady=20)

    def get_stats(self) -> str:
        return f"Player: {self.player.name}, HP: {self.player.health}, Power: {self.player.power}, Block Chance: {self.player.block_chance}, Gold: {self.player.gold}"
    """
    This begins the new scenarios by using the random_scenarios function from game_logic
    This function will then return the necessary information for the UI to display
    The buttons automatically display the options listed within the scenarios dictionary
    
    A noted problem is the rest scenario has one 'missing' action
    The button should be made invisible but I couldn't figure out how to do that
    And I didn't want to use AI for that part because I didn't want to mess with it by that point
    """
    def start_new_scenario(self) -> None:
        self.scenario_counter += 1
        print(self.scenario_counter) # DEBUG - Prints out scenario count to make sure it counts currectly
        # This If statement uses the scenario counter to add player power every 5 scenarios, this is used to create a progression system for the character

        if self.scenario_counter % 5 == 0:
            self.player.power += 10 # Increases player power by 10 every 5 scenarios
            print(f"Power is now {self.player.power}") # DEBUG
            if self.player.block_chance < 50: # Checks if block chance is below 50
                self.player.block_chance += 5 # Adds 5 if it is
            else:
                self.player.block_chance = 50 # Sets it to 50 if it isn't
        self.current_scenario = random_scenarios(self.player) # Function from game_logic.py
        # All below text is what you see in the scenarios frame
        scenario_description = f"{self.current_scenario['description']}\n"
        self.scenario_text.config(state="normal")
        self.scenario_text.delete(1.0, tk.END)
        self.scenario_text.insert(tk.END, scenario_description)
        self.scenario_text.config(state="disabled")

        # Update action buttons based on affordability=(GOLD SCENARIOS) else just leaves the button alone
        for i, (action_name, action) in enumerate(self.current_scenario["results"].items()):
            if self.player.can_afford_action(action):
                self.actions[i].config(text=action_name, state=tk.NORMAL)
            else:
                self.actions[i].config(text=f"{action_name} (Not enough gold)", state=tk.DISABLED)

        # Disable any remaining action buttons (That don't require gold but also aren't present in the scenario)
        for i in range(len(self.current_scenario["results"]), len(self.actions)):
            self.actions[i].config(state=tk.DISABLED)
    def handle_action_ui(self, action_index: int) -> None:
        # Disable action buttons when clicked
        for btn in self.actions:
            btn.config(state=tk.DISABLED)

        # Get the selected action from the current scenario
        action_key = list(self.current_scenario["results"].keys())[action_index]
        action = self.current_scenario["results"][action_key]
        
        # This begins combat and loops through the combat messages until either the enemy or the player is dead
        if "enemy" in action:
            # If the action involves an enemy begin combat
            combat_result = handle_combat(self.player, action["enemy"])

            # Show combat log results in scenario text
            self.scenario_text.config(state="normal")
            self.scenario_text.delete(1.0, tk.END)
            self.scenario_text.insert(tk.END, "\n".join(combat_result["combat_log"]))
            self.scenario_text.config(state="disabled")
            # Ends game when user clicks continue after dying - Defeat Logic
            if combat_result["status"] == "defeat":
                self.scenario_text.config(state="normal")
                self.scenario_text.insert(tk.END, "\n\nYou Have Died")
                self.scenario_text.config(state="disabled")
                self.continue_button.config(state=tk.NORMAL, command=self.end_game)
                return
        else:
            # If the action doesn't involve an enemy, resolve it normally by chance system
            result = game_logic.resolve_action(self.player, action)
            self.scenario_text.config(state="normal")
            self.scenario_text.delete(1.0, tk.END)
            self.scenario_text.insert(tk.END, result["description"])
            self.scenario_text.config(state="disabled")
        # Updates player stats after every scenario.
        self.update_player_stats()

        # Enable continue button
        self.continue_button.config(state=tk.NORMAL)

    def continue_to_next_scenario(self) -> None:
        # Disable continue button before continuing
        self.continue_button.config(state=tk.DISABLED)
        
        # Checks if the player is alive otherwise ends game (Security to make sure the game ends if the player dies outside of combat which is possible)
        if self.player.is_alive():
            self.start_new_scenario()
        else:
            self.end_game()

    def update_player_stats(self) -> None:
        """
        Updates the stats within the UI frame
        Only the Health, Power, and Gold labels are displayed and updated as of now
        There are plans to do block chance in the future but not as of now
        """
        self.health_label.config(text=f"Health: {self.player.health}")
        self.power_label.config(text=f"Power: {self.player.power}")
        self.block_chance_label.config(text=f"Block Chance: {self.player.block_chance}")
        self.gold_label.config(text=f"Gold: {self.player.gold}")
    def end_game(self) -> None:
        # Ends game and closes out
        self.scenario_text.config(state="normal")
        self.scenario_text.delete(1.0, tk.END)
        self.scenario_text.insert(tk.END, "Thanks for playing!")
        self.scenario_text.config(state="disabled")
        self.root.after(2000, self.root.quit)  # Close window after 2 seconds
    def quit_game(self) -> None:

        confirm = messagebox.askyesno("Quit Game", "Are you sure you want to quit?\n\nUnsaved progress will be lost.")
        if confirm:
            self.root.quit()  # Close the window
    def save_game(self) -> None:
        try:
            # My work
            with open("game_data.csv", "w", newline="") as game_file:
                # AI used for a refresher but not as the source
                writer = csv.writer(game_file)
                # I chose rows over columns because it was simpler and could be used if I decided to work on it more to make room for more saves later on
                writer.writerow(["Name", "Health", "Power", "Block Chance", "Gold"])
                writer.writerow([self.player.name, self.player.health, self.player.power, self.player.block_chance, self.player.gold])

                messagebox.showinfo("Game Saved", "Game data saved successfully.")
        except PermissionError: # My work
            messagebox.showerror("Save Error", "Please close out of the csv before saving the game.")
    def load_game(self) -> None:
        """
        Game load logic below:
        This will pull from the game_data.csv file and load the data into the current player's stats.
        As of right now the game data only has room for one save game
        This means it will only pull from one save game at a time
        This also means any save made will overwrite the previous save
        
        The initial generation was done by AI but it didn't work so I weeded out what was broken and fixed it
        I've added notes that say fixed so you can see where I changed any AI code
        Areas without markings were done by me
        """
        try:
            with open("game_data.csv", "r") as game_file:
                reader = csv.reader(game_file)
                
                # Skip header
                header = next(reader, None)
                if not header:
                    messagebox.showerror("Load Error", "Save file is empty!")
                    return

                # Get the data row
                data_row = next(reader, None) # FIXED
                if not data_row or len(data_row) != 5: # FIXED
                    messagebox.showerror("Load Error", "Invalid data in the save file! Information most likely missing or corrupted.")
                    return

                # Validate data types
                try: # AI HELPED
                    name = data_row[0]
                    health = int(data_row[1])
                    power = int(data_row[2])
                    block_chance = int(data_row[3])
                    gold = int(data_row[4])
                except ValueError:
                    messagebox.showerror("Load Error", "Invalid numerical values in the save file!")
                    return

                # Only update player stats if all validations pass
                self.player.name = name
                self.player.health = health
                self.player.power = power
                self.player.block_chance = block_chance
                self.player.gold = gold

                self.update_player_stats() # FIXED, WAS IN THE WRONG ORDER
                self.start_new_scenario()
                messagebox.showinfo("Game Loaded", "Game data loaded successfully!")

            """
            Any errors that occur during loading should be handled below.
            Most common ones have been singled out
            Any miscellaneous/uncommon errors have been accounted for by Exception as e
            """
        except FileNotFoundError:
            messagebox.showerror("Load Error", "Save file not found! Please save a game first.")
        except PermissionError:
            messagebox.showerror("Load Error", "Please close out of the csv before loading the game.")
        except Exception as e:
            print(e)
            messagebox.showerror("Load Error", f"An error occurred while loading the game: {str(e)}")
        # All exceptions were done by me along with all messages

# Fix capitalization and button display
if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
