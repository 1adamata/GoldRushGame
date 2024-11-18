import tkinter as tk



class Drawing:
    def __init__(self, canvas, rows, cols, cell_size):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        #define walls and golds positions
        self.walls = [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (3, 5), (3, 6), (6, 2), (6, 3)]
        self.golds = [(0, 5), (4, 7), (7, 2), (2, 8)]
        self.gold_items = []

        # Draw the grid, walls, and golds
        self.draw_grid()
        self.draw_walls()
        self.draw_golds()

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

    def remove_gold(self, row, col):
        # Find the index of the gold and remove it
        if (row, col) in self.golds:
            index = self.golds.index((row, col))
            self.canvas.delete(self.gold_items[index])
            self.golds.pop(index)
            self.gold_items.pop(index)