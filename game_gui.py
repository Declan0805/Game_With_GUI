import tkinter as tk
from tkinter import ttk, messagebox
import csv
import game_logic
from game_classes import Player
from game_logic import handle_combat, random_scenarios


"""
All buttons and general window information came from me
The aesthetic elements were sourced partly but not entirely by an AI source
Errors in SaveGame and LoadGame logic were partly aided but AI but AI got a decent amount of it wrong so I did most of the work in the end
All Scenario information was done by me unless any major errors occurred in the code that I couldn't weed through
This was the 5th attempt so there was a ton of copy and pasting and major editing to be done from previous versions
This was the first version to be uploaded to github once I decided it was the proper direction
I separated as much logic as I could into gamelogic but while I was in this file I had already,
began work on the savegame and loadgame logic so I just continued here because I was frustrated and wanted it to just work

"""
class GameGUI:
    def __init__(self, root):
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
        self.start_new_scenario()
    def create_widgets(self):
        # AI Sourced
        self.stats_frame = ttk.LabelFrame(self.root, text="Player Stats", padding=10)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # My work
        self.health_label = ttk.Label(self.stats_frame, text=f"Health: {self.player.health}")
        self.health_label.pack(anchor="w")
        # My work
        self.power_label = ttk.Label(self.stats_frame, text=f"Power: {self.player.power}")
        self.power_label.pack(anchor="w")
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

        self.actions = []
        for i in range(3):  # Create up to 3 action buttons
            btn = ttk.Button(self.actions_frame, text=f"Action {i + 1}",
                             command=lambda idx=i: self.handle_action_ui(idx))
            btn.grid(row=0, column=i, padx=10)
            self.actions.append(btn)


        quit_button = ttk.Button(self.actions_frame, text="Quit", command=self.quit_game)
        quit_button.grid(row=1, column=0, padx=10, pady=20)
        save_button = ttk.Button(self.actions_frame, text="Save", command=self.save_game)
        save_button.grid(row=1, column=1, padx=10, pady=20)
        load_button = ttk.Button(self.actions_frame, text="Load", command=self.load_game)
        load_button.grid(row=1, column=2, padx=10, pady=20)

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
    def start_new_scenario(self):
        self.current_scenario = random_scenarios(self.player)
        scenario_description = f"{self.current_scenario['description']}\n"
        self.scenario_text.config(state="normal")
        self.scenario_text.delete(1.0, tk.END)
        self.scenario_text.insert(tk.END, scenario_description)
        self.scenario_text.config(state="disabled")

        for i, action in enumerate(self.current_scenario["results"].keys()):
            self.actions[i].config(text=action, state=tk.NORMAL)

        for i in range(len(self.current_scenario["results"]), len(self.actions)):
            self.actions[i].config(state=tk.DISABLED)
    def handle_action_ui(self, action_index):
        # Get the selected action from the current scenario
        action_key = list(self.current_scenario["results"].keys())[action_index]
        action = self.current_scenario["results"][action_key]
        # This begins combat and loops through the combat messages until either the enemy or the player is dead
        if "enemy" in action:
            # If the action involves combat
            combat_result = handle_combat(self.player, action["enemy"])

            # Show combat log results
            for log_entry in combat_result["combat_log"]:
                messagebox.showinfo("Combat Log", log_entry)
            if combat_result["status"] == "defeat":
                messagebox.showinfo("Game Over", "You Have Died")
                self.end_game()
                return
        else:
            # If the action doesn't involve an enemy, resolve it
            result = game_logic.resolve_action(self.player, action)
            messagebox.showinfo("Action Result", result["description"])

        self.update_player_stats()

        # Checks if the player is alive otherwise ends game and displays end message

        if self.player.is_alive():
            self.start_new_scenario()
        else:
            self.end_game()
    def update_player_stats(self):
        """
        Updates the stats within the UI frame
        Only the Health, Power, and Gold labels are displayed and updated as of now
        There are plans to do block chance in the future but not as of now
        """
        self.health_label.config(text=f"Health: {self.player.health}")
        self.power_label.config(text=f"Power: {self.player.power}")
        self.gold_label.config(text=f"Gold: {self.player.gold}")
    def end_game(self):
        # Ends game and closes out
        messagebox.showinfo("Game Over", "Thanks for playing!")
        self.root.quit()
    def quit_game(self):

        confirm = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
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
            print("Please close out of the csv before saving the game.")
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
    def load_game(self) -> None:
        try:
            with open("game_data.csv", "r") as game_file:
                reader = csv.reader(game_file)

            # Skips the 1st row and then gets the second row to be used for loading data
                header = next(reader, None)

                second_row = next(reader, None)
                # This part was pretty much redone from the ground up because initially it tried to measure length of the columns
                # Then once it did get rows it got the wrong length and made it a print statement
                # I added the not second_row and the len != 5 part so it got the stats needed
                # I also reworked it to pop up an error box so it wouldn't pop up the IDE with the print statement
                if not second_row or len(second_row) != 5:
                    messagebox.showerror("Load Error", "Invalid data in the save file! Information most likely missing or corrupted.")
                    return

                # Loading the stats to the current player's stats
                # This part was done by me
                name, health, power, block_chance, gold = second_row
                self.player.name = name
                self.player.health = int(health)
                self.player.power = int(power)
                self.player.block_chance = int(block_chance)
                self.player.gold = int(gold)

                # AI generated this part but not from a prompt just from autocomplete
                self.update_player_stats()
                self.start_new_scenario()

                messagebox.showinfo("Game Loaded", "Game data loaded successfully!")
            """
            Any errors that occur during loading should be handled below.
            Most common ones have been singled out
            Any miscellaneous/uncommon errors have been accounted for by Exception as e
            """
        except FileNotFoundError:
            messagebox.showerror("Load Error", "Save file not found! Please save a game first.")
        except ValueError as e:
            print(e)
            messagebox.showerror("Load Error", "Invalid numerical values in the save file or there were missing values!")
        except PermissionError:
            messagebox.showerror("Load Error", "Please close out of the csv before loading the game.")
        except Exception as e:
            print(e)
            messagebox.showerror("Load Error", f"An error occurred while loading the game: {str(e)}")
        # All exceptions were done by me along with all messages


if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
