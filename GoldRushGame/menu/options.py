import tkinter as tk
from tkinter import messagebox
from utils import load_controls, save_controls

class Options:
    """
    Represents the Options screen for the Gold Rush Game.
    """

    def __init__(self, root, back_callback):
        """
        Initializes the Options screen with customizable keybindings.

        Args:
            root (tk.Tk): The main Tkinter window where the Options screen is displayed.
            back_callback (function): The function to be called when the back button is pressed.
        """
        self.root = root
        self.controls_file = "controls.json"
        self.controls = load_controls(self.controls_file)
        self.default_controls = {
            "move_up": "Up",
            "move_down": "Down",
            "move_left": "Left",
            "move_right": "Right",
        }
        self.active_entry = None  # Track which entry is currently active

        # Create a label for the Options screen
        options_label = tk.Label(root, text="Options", font=("Helvetica", 24))
        options_label.pack(pady=20)

        # Keybinding customization section
        self.key_entries = {}
        for action in self.controls:
            self.add_keybinding_option(action)

        # Save button to save updated keybindings
        save_button = tk.Button(root, text="Save", font=("Helvetica", 16), command=self.save_controls)
        save_button.pack(pady=10)

        # Revert button to reset keybindings to default values
        revert_button = tk.Button(root, text="Revert", font=("Helvetica", 16), command=self.revert_controls)
        revert_button.pack(pady=10)

        # Back button to return to the main menu
        back_button = tk.Button(root, text="Back", font=("Helvetica", 16), command=back_callback)
        back_button.pack(pady=10)

        # Bind keypress events globally for active entry
        self.root.bind("<KeyPress>", self.on_keypress)

    def add_keybinding_option(self, action):
        """
        Adds a row to the Options screen for customizing a keybinding.

        Args:
            action (str): The name of the action to customize.
        """
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        label = tk.Label(frame, text=f"{action.capitalize()}:", font=("Helvetica", 16))
        label.pack(side=tk.LEFT, padx=10)

        entry = tk.Entry(frame, font=("Helvetica", 16), width=10)
        entry.insert(0, self.controls[action])
        entry.pack(side=tk.LEFT, padx=10)
        entry.bind("<FocusIn>", lambda event, e=entry, a=action: self.set_active_entry(e, a))
        entry.bind("<FocusOut>", lambda event: self.clear_active_entry())
        self.key_entries[action] = entry

    def set_active_entry(self, entry, action):
        """
        Sets the active entry to listen for keypress events.

        Args:
            entry (tk.Entry): The input field where the keybinding is displayed.
            action (str): The action being customized.
        """
        self.active_entry = (entry, action)

    def clear_active_entry(self):
        """
        Clears the active entry when focus is lost.
        """
        self.active_entry = None

    def on_keypress(self, event):
        """
        Handles keypress events for the active entry.

        Args:
            event: The keypress event.
        """
        if self.active_entry:
            entry, action = self.active_entry
            key = event.keysym  # Get the key name
            entry.delete(0, tk.END)  # Clear the current entry field
            entry.insert(0, key)  # Insert the new key name
            self.controls[action] = key  # Update the controls dictionary

    def save_controls(self):
        """
        Saves updated control settings to a JSON file.
        Ensures no duplicate keys are assigned to multiple actions.
        """
        new_controls = {}
        for action, entry in self.key_entries.items():
            key = entry.get().strip()
            if key in new_controls.values():
                messagebox.showerror("Error", f"The key '{key}' is already assigned to another action.")
                return
            new_controls[action] = key

        self.controls = new_controls
        save_controls(self.controls, self.controls_file)

        messagebox.showinfo("Options", "Controls saved successfully!")

    def revert_controls(self):
        """
        Reverts the keybindings to the default values.
        """
        self.controls = self.default_controls.copy()
        for action, entry in self.key_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.controls[action])

        messagebox.showinfo("Options", "Controls reverted to defaults!")