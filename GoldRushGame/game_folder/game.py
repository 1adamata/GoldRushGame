import tkinter as tk
from game_folder.drawing import Drawing
from game_folder.player import Player
from menu.start_game_folder.player_manager import PlayerManager
class GoldRushGame:
    def __init__(self, root, back_callback, selected_player):
        self.root = root
        self.root.title(f"{selected_player}")
        rows = 8
        cols = 10
        cell_size = 50
        self.back_callback = back_callback
        self.paused = False

        # Set up window
        self.canvas = tk.Canvas(self.root, width=cols * cell_size, height=rows * cell_size, bg='black')
        self.canvas.pack()

        #Drawing the grid, walls, golds and moving blocks
        self.grid = Drawing(self.canvas, rows, cols, cell_size)


        # Player setup
        self.manager = PlayerManager("saves.json")
        self.player = Player(self.canvas, self.grid, selected_player, self.manager)

        # Load saved game state
        self.load_game_state(selected_player)

        # Player score display
        self.score_label = tk.Label(self.root, text=f"Score: {self.player.score}", fg="white", bg="black", font=("Arial", 14))
        self.score_label.pack()

        # Add Health label
        self.health_label = tk.Label(self.root, text=f"Health: {self.player.health}", fg="white", bg="black",
                                     font=("Arial", 14))
        self.health_label.pack()

        # Pause menu frame (hidden by default)
        self.pause_menu = tk.Frame(self.root, bg="gray", width=200, height=300)  # Set width and height
        self.pause_menu.place(relx=0.5, rely=0.5, anchor="center")  # Center it on the screen

        # Add some padding or margin inside the pause menu
        self.pause_menu.pack_propagate(False)

        # Pause menu buttons
        self.continue_button = tk.Button(self.pause_menu, text="Continue", font=("Arial", 12), command=self.resume_game)
        self.continue_button.pack(pady=50)

        menu_button = tk.Button(
            self.pause_menu,
            text="Go Back to Menu",
            font=("Arial", 12),
            command=self.go_back_to_menu
        )
        menu_button.pack(pady=50)

        # Initially hide the pause menu
        self.pause_menu.place_forget()

        # Bind keyboard for player movement
        self.root.bind("<KeyPress>", self.on_key_press)

        self.root.bind("<space>", self.toggle_pause)  # Bind Space key for pausing

        # Start moving blocks
        self.move_blocks()

        self.check_player_moving_block_collision()

        # Start gravity effect
        self.apply_gravity()

    def apply_gravity(self):
        """Apply gravity to movable walls and gold."""
        for wall in self.grid.movable_walls:
            wall.fall(self.grid)

        for gold in self.grid.golds:
            gold.fall(self.grid)

        # Call this method again after a short delay
        self.root.after(200, self.apply_gravity)

    def check_player_moving_block_collision(self):
        # Check if the player and any moving block occupy the same position
        for block in self.grid.moving_blocks:
            if block.row == self.player.row and block.col == self.player.col:
                if not self.player.is_invincible:
                    self.player.handle_collision_with_moving_block()
                    self.health_label.config(text=f"Health: {self.player.health}")  # Update health label
                break  # Exit loop after handling collision
        # Schedule the next collision check
        self.root.after(100, self.check_player_moving_block_collision)

    def load_game_state(self, player_name):
        """Restore the saved game state for the player."""
        state = self.manager.load_game_state(player_name)
        if state:
            # Restore player position
            self.player.row = state["player"]["row"]
            self.player.col = state["player"]["col"]
            self.player.score = state["player"]["score"]
            self.player.health = state["player"]["health"]
            self.player.update_position()

            # Restore movable walls
            for wall, wall_state in zip(self.grid.movable_walls, state["movable_walls"]):
                wall.update_position(wall_state["row"], wall_state["col"])

            # Restore moving blocks
            for block, block_state in zip(self.grid.moving_blocks, state["moving_blocks"]):
                block.row = block_state["row"]
                block.col = block_state["col"]
                block.direction = block_state["direction"]
                block.update_position(block_state["row"], block_state["col"])

            # Restore golds
            remaining_gold_positions = {(gold["row"], gold["col"]) for gold in state["golds"]}
            self.grid.golds = [
                gold for gold in self.grid.golds
                if (gold.row, gold.col) in remaining_gold_positions
            ]
    def save_game_state(self):
        """Save the current game state."""
        state = {
            "player": {
                "row": self.player.row,
                "col": self.player.col,
                "score": self.player.score,
                "health": self.player.health,
            },
            "movable_walls": [
                {"row": wall.row, "col": wall.col} for wall in self.grid.movable_walls
            ],
            "moving_blocks": [
                {"row": block.row, "col": block.col, "direction": block.direction} for block in self.grid.moving_blocks
            ],
            "golds": [
                {"row": gold.row, "col": gold.col} for gold in self.grid.golds
            ],  # Save uncollected gold
        }
        self.manager.save_game_state(self.player.name, state)


    def toggle_pause(self, event=None):
        self.paused = not self.paused
        if self.paused:
            self.show_pause_menu()
        else:
            self.hide_pause_menu()

    def show_pause_menu(self):
        self.pause_menu.place(relx=0.5, rely=0.5, anchor="center")
        self.score_label.config(text=f"Score: {self.player.score} (Paused)")

    def hide_pause_menu(self):
        self.pause_menu.place_forget()
        self.score_label.config(text=f"Score: {self.player.score}")

    def resume_game(self):
        self.paused = False
        self.hide_pause_menu()

    def go_back_to_menu(self):
        self.hide_pause_menu()  # Hide the pause menu
        self.back_callback()  # Return to the main menu

    def on_key_press(self, event):
        if event.keysym == "p":  # Use "P" to toggle pause
            self.toggle_pause()
            return

        if self.paused:
            return  # Ignore other inputs when paused
        # Pass walls, movable walls, and golds to the player for interaction
        self.player.move(event, self.grid)
        # Update score and health labels
        self.score_label.config(text=f"Score: {self.player.score}")
        self.health_label.config(text=f"Health: {self.player.health}")

    def move_blocks(self):
        if not self.paused:
            for block in self.grid.moving_blocks:
                block.move(self.grid)
        self.root.after(500, self.move_blocks)  # Adjust timing as needed
