from utils import load_controls
class Player:
    def __init__(self, canvas, grid, player_name, manager):
        self.canvas = canvas
        self.grid = grid
        self.name = player_name
        self.manager = manager

        checkpoint, self.score, self.health = manager.load_player_checkpoint(player_name)
        self.row = checkpoint["row"]
        self.col = checkpoint["col"]
        self.cell_size = grid.cell_size
        self.is_invincible = False  # Invincibility flag
        self.controls = load_controls("controls.json")  # Load controls

        # Create player rectangle at the checkpoint position
        self.player = self.canvas.create_rectangle(
            self.col * self.cell_size,
            self.row * self.cell_size,
            (self.col + 1) * self.cell_size,
            (self.row + 1) * self.cell_size,
            fill='red'
        )

    def move(self, event, grid):
        # Calculate the new position
        new_row, new_col = self.row, self.col
        walls = self.grid.walls
        movable_walls = self.grid.movable_walls
        golds = self.grid.golds
        moving_blocks = self.grid.moving_blocks
        checkpoints = self.grid.checkpoints
        if event.keysym == self.controls['move_up']:
            new_row -= 1
        elif event.keysym == self.controls['move_down']:
            new_row += 1
        elif event.keysym == self.controls['move_left']:
            new_col -= 1
        elif event.keysym == self.controls['move_right']:
            new_col += 1

        # Check if the new position is within grid boundaries
        if not (0 <= new_row < self.grid.rows and 0 <= new_col < self.grid.cols):
            return  # Stop the movement if out of bounds

        # Check collision with walls
        if any(wall.row == new_row and wall.col == new_col for wall in walls):
            return  # Stop movement if there's a wall

        # Check collision with movable walls
        for movable_wall in movable_walls:
            if movable_wall.row == new_row and movable_wall.col == new_col:
                # Try to push the movable wall
                if self.push_movable_wall(movable_wall, event, walls, movable_walls):
                    break  # Wall moved, allow player to move
                return  # Wall cannot be moved, stop player movement

        # Move player if no collision
        self.row, self.col = new_row, new_col
        self.update_position()

        # Check if player is on the same block as a moving block
        for block in moving_blocks:
            if block.row == self.row and block.col == self.col:
                self.handle_collision_with_moving_block()
                break

        # Check for gold collection
        for gold in golds:
            if gold.row == self.row and gold.col == self.col:
                self.collect_gold(gold, golds)
                break

        for checkpoint in checkpoints:
            if checkpoint.row == self.row and checkpoint.col == self.col:
                self.handle_collision_with_checkpoint(checkpoint)
                break

    def handle_collision_with_moving_block(self):
        if not self.is_invincible:
            self.health -= 20
            self.is_invincible = True
            self.canvas.itemconfig(self.player, fill='blue')  # Change color to indicate damage
            # Reset invincibility after 2 seconds
            self.canvas.after(2000, self.reset_invincibility)

    def handle_collision_with_checkpoint(self, checkpoint):
        checkpoint.activate()
        # Save the current game state
        self.manager.save_game_state(
            self.name,
            {
                "player": {
                    "row": self.row,
                    "col": self.col,
                    "score": self.score,
                    "health": self.health,
                },
                "movable_walls": [
                    {"row": wall.row, "col": wall.col} for wall in self.grid.movable_walls
                ],
                "moving_blocks": [
                    {"row": block.row, "col": block.col, "direction": block.direction} for block in
                    self.grid.moving_blocks
                ],
                "golds": [
                    {"row": gold.row, "col": gold.col} for gold in self.grid.golds
                ],  # Save remaining gold
            },
        )
    def reset_invincibility(self):
        self.is_invincible = False
        self.canvas.itemconfig(self.player, fill='red')  # Reset color

    def update_position(self):
        # Calculate new x, y coordinates based on grid position
        x1 = self.col * self.cell_size
        y1 = self.row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Move player to new position
        self.canvas.coords(self.player, x1, y1, x2, y2)

    def collect_gold(self, gold, golds):
        # Remove the gold from the canvas
        self.canvas.delete(gold.object)  # Deletes the visual representation of the gold
        # Remove the gold from the list
        golds.remove(gold)
        # Update the score
        self.score += 1

    def push_movable_wall(self, movable_wall, event, walls, movable_walls):
        # Determine the direction to push the wall
        new_row, new_col = movable_wall.row, movable_wall.col
        if event.keysym == 'Up':
            new_row -= 1
        elif event.keysym == 'Down':
            new_row += 1
        elif event.keysym == 'Left':
            new_col -= 1
        elif event.keysym == 'Right':
            new_col += 1

        # Check if the movable wall can move to the new position
        if (0 <= new_row < self.grid.rows and 0 <= new_col < self.grid.cols and
                not any(wall.row == new_row and wall.col == new_col for wall in walls) and
                not any(mw.row == new_row and mw.col == new_col for mw in movable_walls)):
            movable_wall.update_position(new_row, new_col)
            return True
        return False