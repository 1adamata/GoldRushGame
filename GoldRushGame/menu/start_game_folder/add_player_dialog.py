import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox
from utils import center_window  # Import the center_window function

class AddPlayerDialog:
    def __init__(self, root, add_player_callback, existing_players):
        """
        Initialize the AddPlayerDialog.

        Args:
            root (tk.Tk): The root Tkinter window.
            add_player_callback (function): Callback to add a valid player to the main application.
            existing_players (list): List of current player names for validation.
        """
        self.root = root
        self.add_player_callback = add_player_callback
        self.existing_players = existing_players

        # Create a new Toplevel window for the custom message box
        self.dialog_window = Toplevel(root)
        self.dialog_window.title("Add Player")
        self.dialog_window.geometry("300x150") # Set size of the dialog
        self.dialog_window.resizable(False, False) # Disable resizing

        # Use center_window function from utils to center this dialog
        center_window(self.dialog_window, root, 300, 150)

        #Make the window unmovable
        self.dialog_window.overrideredirect(True)

        #To make dialog always on top
        self.dialog_window.lift()
        self.dialog_window.attributes("-topmost", True)

        #Dialog Label
        self.label = Label(self.dialog_window, text="Enter the player's name:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        #Dialog textbox Entry
        self.player_name_entry = Entry(self.dialog_window, font=("Helvetica", 12))
        self.player_name_entry.pack(pady=5)

        #Buttons for add and cancel
        self.add_button = Button(self.dialog_window, text="Add", font=("Helvetica", 12), command=self.add_player)
        self.add_button.pack(pady=5)
        self.cancel_button = Button(self.dialog_window, text="Cancel", font=("Helvetica", 12), command=self.dialog_window.destroy)
        self.cancel_button.pack(pady=5)

    def add_player(self):
        """
        Validate the player's name and add it if valid.
        """
        player_name = self.player_name_entry.get().strip()
        # Check if the name is unique
        if player_name in self.existing_players:
            messagebox.showerror("Invalid Name", "This player name already exists. Please choose a unique name.")
            return

        # Check if the name meets the character limit
        if len(player_name) > 15:
            messagebox.showerror("Invalid Name", "The player name must be 15 characters or fewer.")
            return

        # Check if the name is not empty
        if not player_name:
            messagebox.showerror("Invalid Name", "The player name cannot be empty.")
            return

        self.add_player_callback(player_name)
        self.dialog_window.destroy()