import tkinter as tk
from drawing import Drawing
from player import Player

class GoldRushGame:
    def __init__(self, korenb):
        self.korenb = korenb
        self.korenb.title("Grid-Based Gold Rush Game")
        ROWS = 8
        COLS = 10
        CELL_SIZE = 50
        # Set up window
        self.canvas = tk.Canvas(self.korenb, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg='black')
        self.canvas.pack()

        #Drawing the grid, walls, and golds
        self.grid = Drawing(self.canvas, ROWS, COLS, CELL_SIZE)

        # Player setup
        self.player = Player(self.canvas, self.grid)

        # Player score display
        self.score_label = tk.Label(self.korenb, text=f"Score: {self.player.score}", fg="white", bg="black", font=("Arial", 14))
        self.score_label.pack()


        # Bind keyboard for player movement
        self.korenb.bind("<KeyPress>", self.on_key_press)



    def on_key_press(self, event):
        # Delegate movement to the Player object
        self.player.move(event, self.grid)
        # Update score label
        self.score_label.config(text=f"Score: {self.player.score}")

if __name__ == "__main__":
    korenb = tk.Tk()
    game = GoldRushGame(korenb)
    korenb.mainloop()
