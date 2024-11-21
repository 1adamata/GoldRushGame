class GameObject:
    def __init__(self, canvas, row, col, cell_size):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.cell_size = cell_size

    def update_position(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        x1 = new_col * self.cell_size
        y1 = new_row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.coords(self.object, x1, y1, x2, y2)


class Wall(GameObject):
    def __init__(self, canvas, row, col, cell_size):
        super().__init__(canvas, row, col, cell_size)
        color = "gray"
        self.object = self.canvas.create_rectangle(
            col * cell_size,
            row * cell_size,
            (col + 1) * cell_size,
            (row + 1) * cell_size,
            fill=color
        )

class MovableWall(GameObject):
    def __init__(self, canvas, row, col, cell_size, direction="horizontal"):
        super().__init__(canvas, row, col, cell_size, )
        self.direction = direction  # "horizontal" or "vertical"
        color = "blue"
        self.object = self.canvas.create_rectangle(
            col * cell_size,
            row * cell_size,
            (col + 1) * cell_size,
            (row + 1) * cell_size,
            fill=color
        )
    def move(self, grid):
        # Determine the next position based on direction
        if self.direction == "horizontal":
            new_col = (self.col + 1) % grid.cols
            self.update_position(self.row, new_col)
        elif self.direction == "vertical":
            new_row = (self.row + 1) % grid.rows
            self.update_position(new_row, self.col)

    def fall(self, grid):
        """Move the wall down if the position below is empty."""
        new_row = self.row + 1
        if new_row < grid.rows and not self.is_collision(grid, new_row, self.col):
            self.update_position(new_row, self.col)

    def is_collision(self, grid, row, col):
        """Check if the wall collides with another object or ground."""
        return (
            (row, col) in [(wall.row, wall.col) for wall in grid.walls] or
            (row, col) in [(gold.row, gold.col) for gold in grid.golds]
        )


class Gold(GameObject):
    def __init__(self, canvas, row, col, cell_size):
        super().__init__(canvas, row, col, cell_size)

        self.object = self.canvas.create_oval(
            col * cell_size + 10,
            row * cell_size + 10,
            (col + 1) * cell_size - 10,
            (row + 1) * cell_size - 10,
            fill="yellow"
        )

    def fall(self, grid):
        """Move the gold down if the position below is empty."""
        new_row = self.row + 1
        if new_row < grid.rows and not self.is_collision(grid, new_row, self.col):
            self.update_position(new_row, self.col)

    def is_collision(self, grid, row, col):
        """Check if the gold collides with another object or ground."""
        return (
            (row, col) in [(wall.row, wall.col) for wall in grid.walls] or
            (row, col) in [(gold.row, gold.col) for gold in grid.golds] or
            (row, col) in [(mw.row, mw.col) for mw in grid.movable_walls]
        )

class MovingBlock(GameObject):
    def __init__(self, canvas, row, col, cell_size, direction="horizontal"):
        super().__init__(canvas, row, col, cell_size)
        self.direction = direction  # "horizontal" or "vertical"
        self.object = self.canvas.create_rectangle(
            col * cell_size,
            row * cell_size,
            (col + 1) * cell_size,
            (row + 1) * cell_size,
            fill="orange"
        )

    def move(self, grid):
        new_row, new_col = self.row, self.col

        if self.direction == "horizontal":
            # Move right
            new_col += 1
            if new_col >= grid.cols or self.is_collision(grid, new_row, new_col):
                # Reverse direction
                self.direction = "left"
            else:
                self.update_position(new_row, new_col)

        elif self.direction == "left":
            # Move left
            new_col -= 1
            if new_col < 0 or self.is_collision(grid, new_row, new_col):
                # Reverse direction
                self.direction = "horizontal"
            else:
                self.update_position(new_row, new_col)

        elif self.direction == "vertical":
            # Move down
            new_row += 1
            if new_row >= grid.rows or self.is_collision(grid, new_row, new_col):
                # Reverse direction
                self.direction = "up"
            else:
                self.update_position(new_row, new_col)

        elif self.direction == "up":
            # Move up
            new_row -= 1
            if new_row < 0 or self.is_collision(grid, new_row, new_col):
                # Reverse direction
                self.direction = "vertical"
            else:
                self.update_position(new_row, new_col)

    def is_collision(self, grid, row, col):
        # Check for collision with static walls or movable walls
        return (
            (row, col) in [(wall.row, wall.col) for wall in grid.walls] or
            (row, col) in [(mw.row, mw.col) for mw in grid.movable_walls]
        )

class Checkpoint(GameObject):
    def __init__(self, canvas, row, col, cell_size):
        super().__init__(canvas, row, col, cell_size)
        self.is_active = False  # Indicates whether the checkpoint is activated
        self.object = self.canvas.create_rectangle(
            col * cell_size,
            row * cell_size,
            (col + 1) * cell_size,
            (row + 1) * cell_size,
            fill="green"
        )

    def activate(self):
        self.is_active = True
        self.canvas.itemconfig(self.object, fill="green")  # Change color to show activation