import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
FPS = 30
HIGH_SCORE_FILE = 'high_scores.txt'
NORMAL_MODE = 0
IMPOSSIBLE_MODE = 1

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")
clock = pygame.time.Clock()

# Initialize the grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Define Tetrominoes
tetrominoes = {
    0: {'shape': [[1, 1, 1, 1]], 'color': (255, 0, 0)},
    1: {'shape': [[1, 1, 1], [0, 1, 0]], 'color': (0, 255, 0)},
    2: {'shape': [[1, 1, 0], [0, 1, 1]], 'color': (0, 0, 255)},
    3: {'shape': [[0, 1, 1], [1, 1, 0]], 'color': (255, 255, 0)},
    4: {'shape': [[1, 1], [1, 1]], 'color': (255, 165, 0)},
    5: {'shape': [[1, 1, 1], [0, 0, 1]], 'color': (75, 0, 130)},
    6: {'shape': [[1, 1, 1], [1, 0, 0]], 'color': (255, 20, 147)}
}

# Tetromino class
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE + j * GRID_SIZE,
                                                          self.y * GRID_SIZE + i * GRID_SIZE,
                                                          GRID_SIZE, GRID_SIZE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def collision(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if self.x + j < 0 or self.x + j >= GRID_WIDTH or self.y + i >= GRID_HEIGHT:
                        return True
                    if grid[self.y + i][self.x + j]:
                        return True
        return False

    def get_ghost_position(self):
        ghost_y = self.y
        while not self.collision_at(self.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def collision_at(self, x, y):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT:
                        return True
                    if grid[y + i][x + j]:
                        return True
        return False

    def draw_ghost(self):
        ghost_y = self.get_ghost_position()
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE + j * GRID_SIZE,
                                                          ghost_y * GRID_SIZE + i * GRID_SIZE,
                                                          GRID_SIZE, GRID_SIZE), 1)

# Function to draw the grid
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

# Function to check and clear full lines
def check_lines():
    global grid
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

# Function to handle game over
def game_over(final_score, final_level, total_lines):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    
    score_text = font.render(f"Score: {final_score}", True, WHITE)
    level_text = font.render(f"Level: {final_level}", True, WHITE)
    lines_text = font.render(f"Lines: {total_lines}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2 + 80))
    screen.blit(lines_text, (SCREEN_WIDTH // 2 - lines_text.get_width() // 2, SCREEN_HEIGHT // 2 - lines_text.get_height() // 2 + 140))
    
    pygame.display.update()
    pygame.time.wait(3000)  # Display game over screen for 3 seconds
    show_game_over_menu()

# Function to show game over menu
def show_game_over_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    exit()

        # Display game over screen until player chooses an option
        draw_text("Press 'R' to Restart or 'Q' to Quit", 36, WHITE, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 100)
        pygame.display.flip()
        clock.tick(FPS)

# Function to reset the game
def reset_game():
    global grid, current_tetromino, next_tetromino, score, level, lines_cleared, total_lines_cleared, gravity_speed, game_mode
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                  random.choice(list(tetrominoes.values()))['color'])
    next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                               random.choice(list(tetrominoes.values()))['color'])
    score = 0
    level = 1
    lines_cleared = 0
    total_lines_cleared = 0
    gravity_speed = 30
    game_mode = NORMAL_MODE

# Function to draw text on the screen
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Function to draw the next tetromino
def draw_next_tetromino(tetromino):
    for i in range(len(tetromino.shape)):
        for j in range(len(tetromino.shape[0])):
            if tetromino.shape[i][j]:
                pygame.draw.rect(screen, tetromino.color, (SCREEN_WIDTH - 120 + j * GRID_SIZE,
                                                          100 + i * GRID_SIZE,
                                                          GRID_SIZE, GRID_SIZE))

# Function to perform a hard drop
def hard_drop(tetromino):
    drop_distance = 0
    while not tetromino.collision():
        tetromino.move(0, 1)
        drop_distance += 1
    tetromino.move(0, -1)
    return drop_distance - 1

# Function to update high scores
def update_high_scores(score, level, lines):
    high_scores = load_high_scores()
    high_scores.append((score, level, lines))
    high_scores.sort(reverse=True, key=lambda x: x[0])  # Sort by score descending
    high_scores = high_scores[:5]  # Keep only top 5 scores
    with open(HIGH_SCORE_FILE, 'w') as f:
        for hs in high_scores:
            f.write(f"{hs[0]},{hs[1]},{hs[2]}\n")

# Function to load high scores
def load_high_scores():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return [tuple(map(int, line.strip().split(','))) for line in f]
    except FileNotFoundError:
        return []

# Function to show high scores
def show_high_scores():
    screen.fill(BLACK)
    draw_text("High Scores", 48, WHITE, SCREEN_WIDTH // 2 - 100, 50)
    high_scores = load_high_scores()
    for i, hs in enumerate(high_scores):
        draw_text(f"{i + 1}. Score: {hs[0]}, Level: {hs[1]}, Lines: {hs[2]}", 36, WHITE, SCREEN_WIDTH // 2 - 200, 150 + i * 50)
    draw_text("Press any key to return to menu", 36, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main game loop
def main():
    global current_tetromino, next_tetromino, score, level, lines_cleared, total_lines_cleared, gravity_speed, game_mode
    current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                  random.choice(list(tetrominoes.values()))['color'])
    next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                               random.choice(list(tetrominoes.values()))['color'])
    score = 0
    level = 1
    lines_cleared = 0
    total_lines_cleared = 0
    gravity_speed = 30
    game_mode = NORMAL_MODE
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        current_tetromino.draw()
        current_tetromino.draw_ghost()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x]:
                    pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_text(f"Score: {score}", 24, WHITE, 10, 10)
        draw_text(f"Level: {level}", 24, WHITE, 10, 40)
        draw_text(f"Lines: {lines_cleared}", 24, WHITE, 10, 70)
        draw_text("Next:", 24, WHITE, SCREEN_WIDTH - 120, 70)
        draw_next_tetromino(next_tetromino)
        draw_text(f"Mode: {'Impossible' if game_mode == IMPOSSIBLE_MODE else 'Normal'}", 24, WHITE, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30)
        draw_text("Press 'M' to switch mode", 18, WHITE, 10, SCREEN_HEIGHT - 30)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0)
                    if current_tetromino.collision():
                        current_tetromino.move(1, 0)
                if event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0)
                    if current_tetromino.collision():
                        current_tetromino.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1)
                    if current_tetromino.collision():
                        current_tetromino.move(0, -1)
                if event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if current_tetromino.collision():
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                if event.key == pygame.K_SPACE:
                    hard_drop(current_tetromino)
                if event.key == pygame.K_m:
                    game_mode = IMPOSSIBLE_MODE if game_mode == NORMAL_MODE else NORMAL_MODE

        current_tetromino.move(0, 1)
        if current_tetromino.collision():
            current_tetromino.move(0, -1)
            for i in range(len(current_tetromino.shape)):
                for j in range(len(current_tetromino.shape[0])):
                    if current_tetromino.shape[i][j]:
                        grid[current_tetromino.y + i][current_tetromino.x + j] = 1
            lines = check_lines()
            score += lines * 100
            lines_cleared += lines
            total_lines_cleared += lines
            if lines_cleared >= 10:
                level += 1
                lines_cleared = 0
                gravity_speed = max(1, gravity_speed - 2)
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                       random.choice(list(tetrominoes.values()))['color'])
            if current_tetromino.collision():
                update_high_scores(score, level, total_lines_cleared)
                game_over(score, level, total_lines_cleared)
                running = False

        clock.tick(gravity_speed)

    pygame.quit()

if __name__ == "__main__":
    main()
