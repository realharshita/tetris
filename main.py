import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
FPS = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")
clock = pygame.time.Clock()

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

tetrominoes = {
    0: {'shape': [[1, 1, 1, 1]], 'color': (255, 0, 0)},
    1: {'shape': [[1, 1, 1], [0, 1, 0]], 'color': (0, 255, 0)},
    2: {'shape': [[1, 1, 0], [0, 1, 1]], 'color': (0, 0, 255)},
    3: {'shape': [[0, 1, 1], [1, 1, 0]], 'color': (255, 255, 0)},
    4: {'shape': [[1, 1], [1, 1]], 'color': (255, 165, 0)},
    5: {'shape': [[1, 1, 1], [0, 0, 1]], 'color': (75, 0, 130)},
    6: {'shape': [[1, 1, 1], [1, 0, 0]], 'color': (255, 20, 147)}
}

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

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

def check_lines():
    global grid
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

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

def reset_game():
    global grid, current_tetromino, next_tetromino, score, level, lines_cleared, total_lines_cleared, gravity_speed
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

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_next_tetromino(tetromino):
    for i in range(len(tetromino.shape)):
        for j in range(len(tetromino.shape[0])):
            if tetromino.shape[i][j]:
                pygame.draw.rect(screen, tetromino.color, (SCREEN_WIDTH - 120 + j * GRID_SIZE,
                                                          100 + i * GRID_SIZE,
                                                          GRID_SIZE, GRID_SIZE))

def hard_drop(tetromino):
    drop_distance = 0
    while not tetromino.collision():
        tetromino.move(0, 1)
        drop_distance += 1
    tetromino.move(0, -1)
    return drop_distance - 1

def update_high_scores(score, level, lines):
    high_scores = load_high_scores()
    high_scores.append((score, level, lines))
    high_scores.sort(reverse=True, key=lambda x: x[0])  # Sort by score descending
    high_scores = high_scores[:10]  # Keep top 10 high scores
    save_high_scores(high_scores)
    return high_scores

def load_high_scores():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            high_scores = [line.strip().split(',') for line in file.readlines()]
            high_scores = [(int(score), int(level), int(lines)) for score, level, lines in high_scores]
            return high_scores
    except FileNotFoundError:
        return []

def save_high_scores(high_scores):
    with open(HIGH_SCORE_FILE, 'w') as file:
        for score, level, lines in high_scores:
            file.write(f"{score},{level},{lines}\n")

def display_high_scores():
    high_scores = load_high_scores()
    if high_scores:
        print("High Scores:")
        for i, (score, level, lines) in enumerate(high_scores, 1):
            print(f"{i}. Score: {score}, Level: {level}, Lines: {lines}")
    else:
        print("No high scores yet.")

def main():
    global current_tetromino, next_tetromino, score, level, lines_cleared, total_lines_cleared, gravity_speed

    current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                  random.choice(list(tetrominoes.values()))['color'])
    next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                               random.choice(list(tetrominoes.values()))['color'])
    score = 0
    level = 1
    lines_cleared = 0
    total_lines_cleared = 0
    gravity_speed = 30

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0)
                    if current_tetromino.collision():
                        current_tetromino.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0)
                    if current_tetromino.collision():
                        current_tetromino.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1)
                    if current_tetromino.collision():
                        current_tetromino.move(0, -1)
                        place_tetromino()
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if current_tetromino.collision():
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                elif event.key == pygame.K_SPACE:
                    drop_distance = hard_drop(current_tetromino)
                    score += drop_distance * 2  # Score calculation for hard drop

        screen.fill(BLACK)
        draw_grid()
        draw_next_tetromino(next_tetromino)
        current_tetromino.draw()
        current_tetromino.draw_ghost()

        if pygame.time.get_ticks() % gravity_speed == 0:
            current_tetromino.move(0, 1)
            if current_tetromino.collision():
                current_tetromino.move(0, -1)
                place_tetromino()

        lines_cleared = check_lines()
        if lines_cleared:
            total_lines_cleared += lines_cleared
            score += (10 * lines_cleared) * level  # Score calculation for lines cleared
            if total_lines_cleared >= level * 10:
                level += 1
                gravity_speed -= 2  # Increase game speed with level

        draw_text(f"Score: {score}", 24, WHITE, 10, 10)
        draw_text(f"Level: {level}", 24, WHITE, 10, 40)
        draw_text(f"Lines: {total_lines_cleared}", 24, WHITE, 10, 70)

        if current_tetromino.collision():
            game_over(score, level, total_lines_cleared)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    HIGH_SCORE_FILE = 'high_scores.txt'
    main()
