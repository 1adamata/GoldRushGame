import tkinter as tk

class StartGameUI:
    def __init__(self, root, back_callback):
        """
        Initializes the Start Game screen with a label and a back button.

        Args:
            root (tk.Tk): The main Tkinter window where the Start Game screen is displayed.
            back_callback (function): The function to be called when the back button is pressed.
        """
        self.root = root
        self.root.title("Start Game")
        self.back_callback = back_callback
         # Create a frame for the start screen
        self.start_game_frame = tk.Frame(root)
        self.start_game_frame.pack()

        # Create a label for Start Game screen
        start_label = tk.Label(
            self.start_game_frame, text="Choose Player", font=("Helvetica", 24)
        )
        start_label.pack(pady=10)

        # Player list box
        self.player_listbox = tk.Listbox(self.start_game_frame, font=("Helvetica", 14), width=50, height=10)
        self.player_listbox.pack(pady=10)

        # Frame to hold the Add and Delete buttons
        self.button_frame = tk.Frame(self.start_game_frame)
        self.button_frame.pack(pady=5)

        # Add Player button in the self.button_frame
        self.add_player_button = tk.Button(self.button_frame, text="Add Player", font=("Helvetica", 14))
        self.add_player_button.grid(row=0, column=0, padx=5)

        # Delete Player button in the self.button_frame
        self.delete_player_button = tk.Button(self.button_frame, text="Delete Player", font=("Helvetica", 14))
        self.delete_player_button.grid(row=0, column=1, padx=5)

        # Play button in the self.frame
        self.play_button = tk.Button(self.start_game_frame, text="Play", font=("Helvetica", 14))
        self.play_button.pack(pady=5)

        # Back button to return to the main menu
        self.back_button = tk.Button(
            self.start_game_frame, text="Back", font=("Helvetica", 14), 
            command=self.back_callback
        )
        self.back_button.pack(pady=5)