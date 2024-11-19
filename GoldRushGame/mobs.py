class Mob:
    def __init__(self, canvas, grid, start_row, start_col, direction='horizontal'):
        self.canvas = canvas
        self.grid = grid
        self.row = start_row
        self.col = start_col
        self.cell_size = grid.cell_size
        self.direction = direction  # 'horizontal' or 'vertical'
        self.move_direction = 1  # 1 for forward, -1 for backward

        # Create mob triangle
        x1, y1, x2, y2 = self.get_coords()
        self.mob = self.canvas.create_polygon(x1, y2, (x1 + x2) / 2, y1, x2, y2, fill='green')

        # Start mob movement
        self.move()

    def get_coords(self):
        # Calculate the coordinates for the mob based on its grid position
        x1 = self.col * self.cell_size
        y1 = self.row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return x1, y1, x2, y2

    def move(self):
        # Determine new position
        if self.direction == 'horizontal':
            new_col = self.col + self.move_direction
            if new_col < 0 or new_col >= self.grid.cols or (self.row, new_col) in self.grid.walls:
                # Reverse direction if hitting wall or boundary
                self.move_direction *= -1
            else:
                self.col = new_col
        elif self.direction == 'vertical':
            new_row = self.row + self.move_direction
            if new_row < 0 or new_row >= self.grid.rows or (new_row, self.col) in self.grid.walls:
                # Reverse direction if hitting wall or boundary
                self.move_direction *= -1
            else:
                self.row = new_row

        # Update mob position
        self.update_position()
        # Schedule next movement
        self.canvas.after(500, self.move)

    def update_position(self):
        # Calculate new coordinates based on grid position
        x1, y1, x2, y2 = self.get_coords()
        # Move mob to new position
        self.canvas.coords(self.mob, x1, y2, (x1 + x2) / 2, y1, x2, y2)
