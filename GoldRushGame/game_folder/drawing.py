from game_folder.game_objects import Wall, MovableWall, Gold, MovingBlock, Checkpoint

class Drawing:
    def __init__(self, canvas, rows, cols, cell_size):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Object collections
        self.walls = []
        self.movable_walls = []
        self.golds = []
        self.moving_blocks = []
        self.checkpoints = []

        # Draw the grid
        self.draw_grid()

        # Initialize objects
        self.initialize_objects()

    def draw_grid(self):
        # Draw horizontal and vertical lines to create grid
        for row in range(self.rows):
            y = row * self.cell_size
            self.canvas.create_line(0, y, self.cols * self.cell_size, y, fill='white')
        for col in range(self.cols):
            x = col * self.cell_size
            self.canvas.create_line(x, 0, x, self.rows * self.cell_size, fill='white')

    def initialize_objects(self):
        # Define static walls
        wall_positions = [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (3, 6), (6, 2), (6, 3)]
        self.walls = [Wall(self.canvas, row, col, self.cell_size) for row, col in wall_positions]

        # Define movable walls
        movable_wall_positions = [(2, 2), (5, 5)]
        directions = ["horizontal", "vertical"]
        self.movable_walls = [
            MovableWall(self.canvas, row, col, self.cell_size, direction)
            for (row, col), direction in zip(movable_wall_positions, directions)
        ]

        # Define gold positions
        gold_positions = [(0, 5), (4, 7), (7, 2), (2, 8)]
        self.golds = [Gold(self.canvas, row, col, self.cell_size) for row, col in gold_positions]

        # Define checkpoint positions
        checkpoint_positions = [(1, 1), (4, 4), (7, 7)]  # Example positions
        self.checkpoints = [Checkpoint(self.canvas, row, col, self.cell_size) for row, col in checkpoint_positions]


        # Define moving blocks
        moving_block_positions = [(3, 4), (7, 8)]
        moving_directions = ["horizontal", "vertical"]
        self.moving_blocks = [
            MovingBlock(self.canvas, row, col, self.cell_size, direction)
            for (row, col), direction in zip(moving_block_positions, moving_directions)
        ]