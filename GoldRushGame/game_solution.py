import tkinter as tk
from drawing import Drawing
from player import Player
from mobs import Mob
from menu import Menu


ROWS = 8
COLS = 10
CELL_SIZE = 50
class GoldRushGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid-Based Gold Rush Game")
        self.menu = Menu(root, self.start_game, self.show_settings)


    def start_game(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Set up window
        self.canvas = tk.Canvas(self.root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg='black')
        self.canvas.pack()

        #Drawing the grid, walls, and golds
        self.grid = Drawing(self.canvas, ROWS, COLS, CELL_SIZE)

        # Player setup
        self.player = Player(self.canvas, self.grid)
        self.player_hp = 100
        self.is_invincible = False

        # Player HP display
        self.hp_label = tk.Label(self.root, text=f"HP: {self.player_hp}", fg="white", bg="black", font=("Arial", 14))
        self.hp_label.pack()

        # Mob setup (adding a few mobs for testing)
        self.mobs = [
            Mob(self.canvas, self.grid, start_row=2, start_col=1, direction='horizontal'),
            Mob(self.canvas, self.grid, start_row=5, start_col=5, direction='vertical')
        ]

        # Player score display
        self.score_label = tk.Label(self.root, text=f"Score: {self.player.score}", fg="white", bg="black", font=("Arial", 14))
        self.score_label.pack()


        # Bind keyboard for player movement
        self.root.bind("<KeyPress>", self.on_key_press)
        
        # Check for collisions periodically
        self.check_collision()


    def show_settings(self):
        self.menu.show_settings()

    def on_key_press(self, event):
        # Delegate movement to the Player object
        self.player.move(event, self.grid)

        # Update score label
        self.score_label.config(text=f"Score: {self.player.score}")

    def check_collision(self):
        # Check for collision between player and mobs based on grid position
        if not self.is_invincible:
            for mob in self.mobs:
                if self.player.row == mob.row and self.player.col == mob.col:
                    self.handle_collision()
                    break

        # Schedule the next collision check
        self.root.after(100, self.check_collision)

    def handle_collision(self):
        # Player takes damage and becomes invincible for 2 seconds
        self.player_hp -= 20
        self.hp_label.config(text=f"HP: {self.player_hp}")
        self.is_invincible = True
        self.canvas.itemconfig(self.player.player, fill='blue')
        # Check if player HP is 0
        if self.player_hp <= 0:
            self.game_over()
        else:
            # Schedule invincibility to wear off after 2 seconds
            self.root.after(2000, self.remove_invincibility)


    def remove_invincibility(self):
        self.is_invincible = False
        self.canvas.itemconfig(self.player.player, fill='red')

    def game_over(self):
        # Clear the canvas and display game over message
        self.canvas.delete("all")
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 - 20, 
                                text="GAME OVER", fill="white", font=("Arial", 24))
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 + 20, 
                                text=f"Score: {self.player.score}", fill="white", font=("Arial", 18))

if __name__ == "__main__":
    root = tk.Tk()
    game = GoldRushGame(root)
    root.mainloop()
