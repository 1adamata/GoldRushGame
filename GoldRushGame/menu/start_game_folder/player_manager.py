import json
import os
import tkinter as tk

class PlayerManager:
    def __init__(self, player_file="saves.json"):
        self.player_file = player_file

    def save_game_state(self, player_name, state):
        """Save the player's current game state, including score and gold positions."""
        players = self.load_all_players()
        for player in players:
            if player["name"] == player_name:
                player["game_state"] = state
                player["score"] = state["player"]["score"]
                break
        with open(self.player_file, "w") as file:
            json.dump(players, file)

    def load_game_state(self, player_name):
        """Load the player's saved game state."""
        if os.path.exists(self.player_file):
            with open(self.player_file, "r") as file:
                players = json.load(file)
                for player in players:
                    if player["name"] == player_name:
                        return player.get("game_state", None)
        return None

    def load_players(self, listbox):
        """Load players from the JSON file and display them in the Listbox."""
        if os.path.exists(self.player_file):
            try:
                with open(self.player_file, "r") as file:
                    players = json.load(file)
                    for player in players:
                        listbox.insert(tk.END, f"{player['name']} - Progress: {player['progress']} - Score: {player['score']}")
            except (json.JSONDecodeError, ValueError):
                with open(self.player_file, "w") as file:
                    json.dump([], file)

    def load_all_players(self):
        """Load all players from the JSON file."""
        if os.path.exists(self.player_file):
            with open(self.player_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []  # Return an empty list if the file is corrupted
        return []  # Return an empty list if the file does not exist

    def update_player_checkpoint(self, player_name, row, col, score, health):
        """Update the player's checkpoint, score, and health."""
        players = self.load_all_players()
        for player in players:
            if player["name"] == player_name:
                player["checkpoint"] = {"row": row, "col": col}
                player["score"] = score
                player["health"] = health
                break
        with open(self.player_file, "w") as file:
            json.dump(players, file)

    def load_player_checkpoint(self, player_name):
        """Load the player's last checkpoint."""
        if os.path.exists(self.player_file):
            with open(self.player_file, "r") as file:
                players = json.load(file)
                for player in players:
                    if player["name"] == player_name:
                        return player.get("checkpoint", {"row": 0, "col": 0}), player.get("score", 0), player.get("health", 100)
        return {"row": 0, "col": 0}, 0, 100

    def save_players(self, listbox):
        """Save the current list of players to a JSON file."""
        players = []
        for i in range(listbox.size()):
            player_info = listbox.get(i).split(' - ')
            name = player_info[0]
            progress = int(player_info[1].split(': ')[1])
            score = int(player_info[2].split(': ')[1])
            players.append({"name": name, "progress": progress, "score": score})
        with open(self.player_file, "w") as file:
            json.dump(players, file)