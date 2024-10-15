import pygame
import random

# Constants
BLOCK_SIZE = 30
ROWS = 20
COLS = 10
SCREEN_WIDTH = COLS * BLOCK_SIZE
SCREEN_HEIGHT = ROWS * BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tetromino shapes
TETROMINOS = [
    [[1, 1, 1, 1]],  # Line
    [[1, 1], [1, 1]],  # Square
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
]

# Tetromino class
class Tetromino:
    def __init__(self):
        self.shape = random.choice(TETROMINOS)
        self.color = RED  # All falling blocks are red initially
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def is_valid_move(self, grid):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # There's a block here
                    new_x = self.x + col_idx
                    new_y = self.y + row_idx
                    # Check if within bounds or colliding with a locked block
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                        return False
        return True

    def get_positions(self):
        positions = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    positions.append((self.x + col_idx, self.y + row_idx))
        return positions

# Create grid function
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

# Clear rows function
def clear_rows(grid, locked_positions):
    cleared_rows = 0
    for i in range(ROWS - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:  # Row is full
            cleared_rows += 1
            del grid[i]
            grid.insert(0, [BLACK] * COLS)

            # Keep the same locked positions without moving the blocks
            keys_to_remove = [k for k in locked_positions if k[1] == i]
            for k in keys_to_remove:
                del locked_positions[k]

    return cleared_rows

def display_title(screen):
    pygame.init()
    font = pygame.font.SysFont('Arial', 50)
    title_text = font.render("TETRIS", True, (255, 255, 255))
    
    # Fill the screen with black and display the title
    screen.fill((0, 0, 0))
    screen.blit(title_text, (COLS * BLOCK_SIZE // 2 - title_text.get_width() // 2, ROWS * BLOCK_SIZE // 4))
    
    pygame.display.update()

    # Wait for 2 seconds or until a key is pressed
    pygame.time.delay(2000)



# Game loop
def run_game():
    pygame.init()
    pygame.display.set_caption("TETRIS")  # Set window title to "TETRIS"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display_title(screen) 
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 25)
    
    running = True
    grid = create_grid()
    current_tetromino = Tetromino()
    locked_positions = {}
    score = 0
    fall_time = 0
    fall_speed = 0.5  # Fall every half a second

    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            current_tetromino.move_down()
            if not current_tetromino.is_valid_move(grid):
                current_tetromino.y -= 1
                for pos in current_tetromino.get_positions():
                    locked_positions[(pos[0], pos[1])] = BLUE  # Change block to blue after collision
                current_tetromino = Tetromino()
                if not current_tetromino.is_valid_move(grid):
                    running = False  # Game over
            fall_time = 0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_left()
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.move_right()
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_right()
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.move_left()
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move_down()
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.y -= 1
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.rotate()  # Undo rotation

        # Clear full rows and update score
        cleared_rows = clear_rows(grid, locked_positions)
        score += cleared_rows * 100

        # Draw grid
        screen.fill(BLACK)
        for row_idx, row in enumerate(grid):
            for col_idx, color in enumerate(row):
                if color != BLACK:
                    pygame.draw.rect(screen, color, pygame.Rect(col_idx * BLOCK_SIZE, row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw current tetromino
        for pos in current_tetromino.get_positions():
            pygame.draw.rect(screen, current_tetromino.color, pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run_game()
