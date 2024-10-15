import random

BLOCK_SIZE = 30
ROWS = 20
COLS = 10

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tetromino shapes
TETROMINOS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(TETROMINOS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.color = random.choice([BLUE, RED])  # Assign a random color

    def move_down(self):
        self.y += 1

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def is_valid_move(self, grid):
        """ Check if the current position of the tetromino is valid. """
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = self.x + col_idx
                    new_y = self.y + row_idx
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or grid[new_y][new_x]:
                        return False
        return True

    def get_positions(self):
        """ Returns the list of all grid positions occupied by the tetromino. """
        positions = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    positions.append((self.x + col_idx, self.y + row_idx))
        return positions

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

    # Add locked positions to the grid
    for (x, y), color in locked_positions.items():
        grid[y][x] = color

    return grid

def check_collision(grid, tetromino):
    """ Check if the tetromino collides with the grid boundaries or placed blocks. """
    for row_idx, row in enumerate(tetromino.shape):
        for col_idx, cell in enumerate(row):
            if cell:  # If there is a block in the tetromino at (row_idx, col_idx)
                new_x = tetromino.x + col_idx
                new_y = tetromino.y + row_idx
                # Check for boundary or block collision
                if new_x < 0 or new_x >= COLS or new_y >= ROWS or grid[new_y][new_x]:
                    return True
    return False

def lock_tetromino(grid, tetromino):
    """ Lock the tetromino into the grid when it reaches the bottom or collides with another tetromino. """
    for row_idx, row in enumerate(tetromino.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                grid[tetromino.y + row_idx][tetromino.x + col_idx] = 1

def clear_rows(grid, locked):
    cleared_rows = 0
    for i in range(ROWS):
        row = grid[i]
        if (0, 0, 0) not in row:
            cleared_rows += 1
            del grid[i]
            grid.insert(0, [(0, 0, 0)] * COLS)
    return cleared_rows

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1

def draw_ui(screen, game_state, font):
    """ Draws the score and level on the screen. """
    score_text = font.render(f"Score: {game_state.score}", True, WHITE)
    level_text = font.render(f"Level: {game_state.level}", True, WHITE)
    screen.blit(score_text, (COLS * BLOCK_SIZE + 10, 20))
    screen.blit(level_text, (COLS * BLOCK_SIZE + 10, 50))
