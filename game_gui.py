import tkinter as tk
from tkinter import ttk, messagebox

import game_logic
from game_classes import Player, Enemy
from game_logic import handle_combat, random_scenarios

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game GUI")
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
        quit_button.grid(row=0, column=3, padx=10)

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
            combat_result = game_logic.handle_combat(self.player, action["enemy"])

            # Show combat log results
            for log_entry in combat_result["combat_log"]:
                messagebox.showinfo("Combat Log", log_entry)
            if combat_result["status"] == "defeat":
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
            # Load the next scenario if the player is alive
            self.start_new_scenario()
        else:
            # End the game if the player is dead
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


if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
