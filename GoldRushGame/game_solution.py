"""
This script initializes and launches the Gold Rush Game's main menu interface.

Modules:
    tkinter (tk): Provides the GUI functionality for the main application window.
    MainMenu: A class that creates the main menu interface for the Gold Rush Game.

Usage:
    Run this script directly to display the main menu of the Gold Rush Game.
"""

import tkinter as tk
from menu.main_menu import MainMenu

if __name__ == "__main__":
    root = tk.Tk()
    game_menu = MainMenu(root)
    root.mainloop()

