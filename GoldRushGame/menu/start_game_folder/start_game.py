import tkinter as tk
from tkinter import messagebox

from game_folder.game import GoldRushGame
from menu.start_game_folder.add_player_dialog import AddPlayerDialog
from menu.start_game_folder.player_manager import PlayerManager
from menu.start_game_folder.start_game_ui import StartGameUI


class StartGame:
    """
    Represents the Start Game screen for the Gold Rush Game.

    This screen initiates the game_folder interface, displaying a start label and
    a back button to return to the main menu.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        back_callback (function): Callback function to return to the main menu.
    """

    def __init__(self, root, back_callback):
        #UI config
        self.back_callback = back_callback
        self.ui = StartGameUI(root, back_callback)
        self.ui.add_player_button.config(command=self.show_add_player_dialog)
        self.ui.delete_player_button.config(command=self.delete_player)
        self.ui.play_button.config(command=self.start_game)

        #player manager
        self.player_file = "saves.json"
        self.manager = PlayerManager(self.player_file)
        self.manager.load_players(self.ui.player_listbox)


    def show_add_player_dialog(self):
        #take existing player names
        existing_players =  [self.ui.player_listbox.get(i).split(' - ')[0] for i in range(self.ui.player_listbox.size())]

        #add player Dialog
        AddPlayerDialog(self.ui.root, self.add_player, existing_players)


    def add_player(self, player_name):
        """
        Add a valid player to the player list and save to the file.
        """
        self.ui.player_listbox.insert(tk.END, f"{player_name} - Progress: 0 - Score: 0")
        self.manager.save_players(self.ui.player_listbox)


    def delete_player(self):
        """Delete the selected player from the listbox and save changes."""
        try:
            # Get the selected player
            selected_index = self.ui.player_listbox.curselection()[0]
            selected_player = self.ui.player_listbox.get(selected_index)
            
            # Confirm deletion
            confirm = messagebox.askyesno("Delete Player", f"Are you sure you want to delete '{selected_player.split(' - ')[0]}'?")
            if confirm:
                # Delete player from the listbox
                self.ui.player_listbox.delete(selected_index)
                self.manager.save_players(self.ui.player_listbox)  # Save changes to the file
        except IndexError:
            messagebox.showerror("Delete Error", "Please select a player to delete.")  

    def start_game(self):
        """Start the game_folder with the selected player."""
        try:
            # Get the selected player
            selected_index = self.ui.player_listbox.curselection()[0]
            selected_player = self.ui.player_listbox.get(selected_index).split(' - ')[0]

            #delete all widgets in the start game_folder page
            for widget in self.ui.root.winfo_children():
                widget.pack_forget()

            #start the game_folder
            GoldRushGame(self.ui.root, self.back_callback, selected_player)
        except IndexError:
            messagebox.showerror("Start Game Error", "Please select a player to start the game_folder.")

            