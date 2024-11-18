class Player:
    def __init__(self, canvas, grid):
        self.canvas = canvas
        self.grid = grid
        self.row = 0
        self.col = 0
        self.cell_size = grid.cell_size
        self.score = 0

        # Create player rectangle
        self.player = self.canvas.create_rectangle(0, 0, self.cell_size, self.cell_size, fill='red')

    def move(self, event, grid):
        # Calculate new potential position
        new_row = self.row
        new_col = self.col
        if event.keysym == 'Up':
            new_row -= 1
        elif event.keysym == 'Down':
            new_row += 1
        elif event.keysym == 'Left':
            new_col -= 1
        elif event.keysym == 'Right':
            new_col += 1

        # Check if the new position is within bounds and not a wall
        if (0 <= new_row < grid.rows and 0 <= new_col < grid.cols and
                (new_row, new_col) not in grid.walls):
            # Update player position
            self.row = new_row
            self.col = new_col
            self.update_position()

            # Check if player has collected a gold
            if (self.row, self.col) in grid.golds:
                self.collect_gold(grid)

    def update_position(self):
        # Calculate new x, y coordinates based on grid position
        x1 = self.col * self.cell_size
        y1 = self.row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Move player to new position
        self.canvas.coords(self.player, x1, y1, x2, y2)

    def collect_gold(self, grid):
        # Remove the gold from the grid
        grid.remove_gold(self.row, self.col)
        # Update score
        self.score += 1
