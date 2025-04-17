import tkinter as tk
from tkinter import ttk, messagebox
import csv
import game_logic
from game_classes import Player, Enemy
from game_logic import handle_combat, random_scenarios

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game GUI")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.player = Player("Hero", health=100, power=20, block_chance=25, gold=0)
        self.enemy = None
        self.create_widgets()
        self.start_new_scenario()
    def create_widgets(self):
        self.stats_frame = ttk.LabelFrame(self.root, text="Player Stats", padding=10)
        self.stats_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.health_label = ttk.Label(self.stats_frame, text=f"Health: {self.player.health}")
        self.health_label.pack(anchor="w")

        self.power_label = ttk.Label(self.stats_frame, text=f"Power: {self.player.power}")
        self.power_label.pack(anchor="w")

        self.gold_label = ttk.Label(self.stats_frame, text=f"Gold: {self.player.gold}")
        self.gold_label.pack(anchor="w")

        # Scenario description frame
        self.scenario_frame = ttk.LabelFrame(self.root, text="Scenario", padding=10)
        self.scenario_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.scenario_text = tk.Text(self.scenario_frame, width=50, height=10, wrap=tk.WORD, state="disabled")
        self.scenario_text.pack()

        # Action buttons
        self.actions_frame = ttk.Frame(self.root)
        self.actions_frame.grid(row=1, column=0, columnspan=3, pady=20)

        self.actions = []
        for i in range(3):  # Create up to 3 action buttons
            btn = ttk.Button(self.actions_frame, text=f"Action {i + 1}",
                             command=lambda idx=i: self.handle_action_ui(idx))
            btn.grid(row=0, column=i, padx=10)
            self.actions.append(btn)

        # Add Quit button
        quit_button = ttk.Button(self.actions_frame, text="Quit", command=self.quit_game)
        quit_button.grid(row=1, column=0, padx=10, pady=20)
        save_button = ttk.Button(self.actions_frame, text="Save", command=self.save_game)
        save_button.grid(row=1, column=1, padx=10, pady=20)
        save_button = ttk.Button(self.actions_frame, text="Load", command=self.load_game)
        save_button.grid(row=1, column=2, padx=10, pady=20)

    def get_stats(self):
        return f"Player: {self.player.name}, HP: {self.player.health}, Power: {self.player.power}, Block Chance: {self.player.block_chance}, Gold: {self.player.gold}"

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

        # Update player stats in the UI after resolving the action
        self.update_player_stats()

        # Check if the player is still alive
        if self.player.is_alive():
            self.start_new_scenario()
        else:
            self.end_game()
    def update_player_stats(self):
        """Updates the player stats in the UI."""
        self.health_label.config(text=f"Health: {self.player.health}")
        self.power_label.config(text=f"Power: {self.player.power}")
        self.gold_label.config(text=f"Gold: {self.player.gold}")
    def end_game(self):
        """Ends the game and closes the application."""
        messagebox.showinfo("Game Over", "Thanks for playing!")
        self.root.quit()
    def quit_game(self):
        """Safely quit the game."""
        confirm = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
        if confirm:
            self.root.quit()  # Close the application
    def save_game(self):
        try:
            with open("game_data.csv", "w", newline="") as game_file:
                writer = csv.writer(game_file)

                writer.writerow(["Name", "Health", "Power", "Block Chance", "Gold"])
                writer.writerow([self.player.name, self.player.health, self.player.power, self.player.block_chance, self.player.gold])

                messagebox.showinfo("Game Saved", "Game data saved successfully.")
        except PermissionError:
            print("Please close out of the csv before saving the game.")
    def load_game(self):
        try:
            print("Attempting to load data from game_data.csv...")

            with open("game_data.csv", "r") as game_file:
                reader = csv.reader(game_file)
                header = next(reader, None)  # Skip the header row

                # Debug: Ensure the header row is as expected
                print(f"Header read: {header}")

                # Dictionary to store player data
                player_data = {}

                # Read the body of the file
                for row in reader:
                    # Debug: Check each row being processed
                    print(f"Processing row: {row}")

                    if row and len(row) == 2:  # Ensure valid key-value rows
                        key, value = row

                        # Map stats to player attributes
                        if key in ["Health", "Power", "Block Chance", "Gold"]:
                            player_data[key.lower().replace(" ", "_")] = int(value)
                        elif key == "Name":
                            player_data["name"] = value

                # Debug: Output the loaded data
                print("Loaded player_data:", player_data)

                # Update the player object
                if player_data:
                    self.player.name = player_data.get("name", "Hero")
                    self.player.health = player_data.get("health", 100)
                    self.player.power = player_data.get("power", 20)
                    self.player.block_chance = player_data.get("block_chance", 25)
                    self.player.gold = player_data.get("gold", 0)

                    # Debug: Confirm player object has been updated
                    print("Updated player stats:",
                          self.player.name, self.player.health, self.player.power, self.player.block_chance,
                          self.player.gold)

                    # Update UI to reflect loaded stats
                    self.update_player_stats()

                    # Debug: Ensure stats frame has been updated
                    print("Player stats displayed in UI have been updated.")

                    self.start_new_scenario()
                    messagebox.showinfo("Game Loaded", "Game data loaded successfully.")
                else:
                    messagebox.showerror("Load Error", "No valid data was loaded!")
        except FileNotFoundError:

            messagebox.showerror("Load Error", "Save file not found! Please save a game first.")
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading the game: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
