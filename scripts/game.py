import pygame
from scripts.tetris_logic import Tetromino, create_grid, clear_rows, BLOCK_SIZE, ROWS, COLS, BLUE

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
    clock = pygame.time.Clock()
    running = True
    current_tetromino = Tetromino()
    locked_positions = {}
    grid = create_grid(locked_positions)  # Initialize the grid with locked positions
    score = 0  # Initialize score
    fall_time = 0  # Track time for gravity (automatic downward movement)
    fall_speed = 0.5  # Control how fast the tetromino falls (lower value means faster fall)

    while running:
        grid = create_grid(locked_positions)  # Update grid with locked positions
        fall_time += clock.get_rawtime()  # Accumulate time for gravity
        clock.tick()  # Reset clock for next iteration

        # Automatically move tetromino down based on fall_time and fall_speed (gravity)
        if fall_time / 1000 >= fall_speed:
            current_tetromino.y += 1  # Move tetromino down
            if not current_tetromino.is_valid_move(grid):
                current_tetromino.y -= 1  # Undo the move if it collides
                # Lock tetromino in place and spawn a new one
                for pos in current_tetromino.get_positions():
                    locked_positions[(pos[0], pos[1])] = current_tetromino.color
                current_tetromino = Tetromino()
                if not current_tetromino.is_valid_move(grid):  # Check if the new tetromino can move
                    running = False  # Game over condition
            fall_time = 0  # Reset fall timer

        # Event handling (key presses for left, right, rotate, and faster fall)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.x += 1  # Undo if invalid
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.x -= 1  # Undo if invalid
                elif event.key == pygame.K_DOWN:  # Manually speed up the fall
                    current_tetromino.y += 1
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.y -= 1  # Undo if invalid
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if not current_tetromino.is_valid_move(grid):
                        current_tetromino.rotate()  # Undo rotation if invalid

        # Clear rows if they are filled and update score
        cleared_rows = clear_rows(grid, locked_positions)
        score += cleared_rows * 100  # Add 100 points for each cleared row

        # Draw the grid and tetrominoes
        screen.fill((0, 0, 0))  # Clear the screen
        for row_idx, row in enumerate(grid):
            for col_idx, color in enumerate(row):
                if color != (0, 0, 0):  # Only draw non-empty blocks
                    pygame.draw.rect(screen, color, pygame.Rect(col_idx * BLOCK_SIZE, row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw the current falling tetromino
        for pos in current_tetromino.get_positions():
            pygame.draw.rect(screen, current_tetromino.color, pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Display score
        font = pygame.font.SysFont('Arial', 25)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)  # Limit game speed to 10 frames per second

    pygame.quit()
