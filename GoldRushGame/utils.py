import json

def load_controls(file_path="controls.json"):
    """
    Loads control settings from a JSON file or initializes default settings.

    Args:
        file_path (str): Path to the JSON file containing controls configuration.

    Returns:
        dict: Dictionary of controls with actions mapped to keys.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Default controls
        return {
            "move_up": "Up",
            "move_down": "Down",
            "move_left": "Left",
            "move_right": "Right",
        }

def save_controls(controls, file_path="controls.json"):
    """
    Saves control settings to a JSON file.

    Args:
        controls (dict): Dictionary of controls with actions mapped to keys.
        file_path (str): Path to the JSON file where controls should be saved.
    """
    with open(file_path, "w") as file:
        json.dump(controls, file, indent=4)

def center_window(window, parent, width, height):
    """Center a window on its parent window."""
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    # Calculate position to center the window
    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    # Set the window's position
    window.geometry(f"{width}x{height}+{x}+{y}")