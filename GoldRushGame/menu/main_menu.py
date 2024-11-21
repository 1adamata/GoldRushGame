import tkinter as tk
from tkinter import messagebox
from menu.options import Options
from menu.start_game_folder.start_game import StartGame

class MainMenu:
    """
    This class creates a main menu interface with buttons to start the game_folder, options,
    and quit the game_folder.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        title_label (tk.Label): The title label displaying the game_folder name.
        start_button (tk.Button): Button to start the game_folder.
        options_button (tk.Button): Button to show the options menu.
        quit_button (tk.Button): Button to quit the game_folder.
    """


    def __init__(self, root):
        """
        Initializes the main menu with a title, size, and control buttons.

        Args:
            root (tk.Tk): The main Tkinter window where the menu is displayed.
        """
        self.root = root

        #creating a main window
        self.root.title("Game Menu") #title of window
        self.root.geometry("600x500") #size of window
        self.root.resizable(False, False)  # Prevent resizing of the window

        #Frame to hold all elements
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=50)

        # Create title label
        self.title_label = tk.Label(
            self.menu_frame, text="Gold Rush", font=("Helvetica", 40)
        )
        self.title_label.grid(row=0, column=0, pady=30)

        # Start Game button
        self.start_button = tk.Button(
            self.menu_frame, text="Start Game", font=("Helvetica", 16), 
            command=self.start_game
        )
        self.start_button.grid(row=1, column=0, pady=10)

        # Options button
        self.options_button = tk.Button(
            self.menu_frame, text="Options", font=("Helvetica", 16),
            command=self.show_options
        )
        self.options_button.grid(row=2, column=0, pady=10)

        # Quit button
        self.quit_button = tk.Button(
            self.menu_frame, text="Quit", font=("Helvetica", 16),
            command=self.quit_game
        )
        self.quit_button.grid(row=3, column=0, pady=10)

    def start_game(self):
        """Starts the game_folder by clearing the main menu and initializing the game_folder interface."""
        self.clear_menu()
        StartGame(self.root, self.back_to_main_menu)
        
    def show_options(self):
        """Displays the options menu by clearing the main menu and initializing the options interface."""
        self.clear_menu()
        Options(self.root, self.back_to_main_menu)

    def clear_menu(self):
        """Clears the main menu by hiding all menu widgets."""
        self.menu_frame.pack_forget()

    
    def back_to_main_menu(self):
        """Returns to the main menu by clearing any current widgets and displaying the main menu widgets."""
        # Clear the current menu
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Recreate the main menu
        self.menu_frame.pack(pady=5)

    def quit_game(self):
        """Prompts the user for confirmation to quit the game_folder and exits if confirmed."""
        answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if answer:
            self.root.quit()