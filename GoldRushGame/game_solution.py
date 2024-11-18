import tkinter as tk

class GridBasedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid-Based Diamond Rush Game with Walls and Gold")

        # Define grid dimensions (e.g., 8x10 grid)
        self.rows = 8
        self.cols = 10
        self.cell_size = 50  # Each cell is 50x50 pixels

        # Set up canvas
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='black')
        self.canvas.pack()

        # Draw the grid (for visualization)
        self.draw_grid()

        # Define walls (as (row, col) tuples)
        self.walls = [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (3, 5), (3, 6), (6, 2), (6, 3)]
        self.draw_walls()

        # Define gold positions (as (row, col) tuples)
        self.golds = [(0, 5), (4, 7), (7, 2), (2, 8)]
        self.gold_items = []  # To keep track of canvas gold item objects
        self.draw_golds()

        # Player setup (starting at row 0, col 0)
        self.player_row = 0
        self.player_col = 0
        self.player = self.canvas.create_rectangle(0, 0, self.cell_size, self.cell_size, fill='red')

        # Player score
        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", fg="white", bg="black", font=("Arial", 14))
        self.score_label.pack()

        # Bind keyboard for player movement
        self.root.bind("<KeyPress>", self.on_key_press)

    def draw_grid(self):
        # Draw horizontal and vertical lines to create grid
        for row in range(self.rows):
            y = row * self.cell_size
            self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill='white')
        for col in range(self.cols):
            x = col * self.cell_size
            self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill='white')

    def draw_walls(self):
        # Draw walls as filled rectangles on the canvas
        for (row, col) in self.walls:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray')

    def draw_golds(self):
        # Draw golds as filled circles (ovals) on the canvas
        for (row, col) in self.golds:
            x1 = col * self.cell_size + 10
            y1 = row * self.cell_size + 10
            x2 = x1 + self.cell_size - 20
            y2 = y1 + self.cell_size - 20
            gold_item = self.canvas.create_oval(x1, y1, x2, y2, fill='yellow')
            self.gold_items.append(gold_item)

    def on_key_press(self, event):
        # Calculate new potential position based on arrow key presses
        new_row = self.player_row
        new_col = self.player_col
        if event.keysym == 'Up':
            new_row -= 1
        elif event.keysym == 'Down':
            new_row += 1
        elif event.keysym == 'Left':
            new_col -= 1
        elif event.keysym == 'Right':
            new_col += 1

        # Check if the new position is within bounds and not a wall
        if (0 <= new_row < self.rows and 0 <= new_col < self.cols and
                (new_row, new_col) not in self.walls):
            # Update player position
            self.player_row = new_row
            self.player_col = new_col
            self.update_player_position()

            # Check if player has collected a gold
            if (self.player_row, self.player_col) in self.golds:
                self.collect_gold(self.player_row, self.player_col)

    def update_player_position(self):
        # Calculate the new x, y coordinates based on grid position
        x1 = self.player_col * self.cell_size
        y1 = self.player_row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Move player to new position
        self.canvas.coords(self.player, x1, y1, x2, y2)

    def collect_gold(self, row, col):
        # Find the index of the collected gold
        index = self.golds.index((row, col))
        
        # Remove the gold from canvas and list
        self.canvas.delete(self.gold_items[index])
        self.golds.pop(index)
        self.gold_items.pop(index)

        # Update score
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GridBasedGame(root)
    root.mainloop()
