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

# Load sound effects
line_clear_sound = pygame.mixer.Sound('line_clear.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

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

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

def check_lines():
    global grid
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    if full_lines:
        line_clear_sound.play()
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

def game_over(final_score, final_level):
    game_over_sound.play()
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))
    
    score_text = font.render(f"Score: {final_score}", True, WHITE)
    level_text = font.render(f"Level: {final_level}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2 + 80))
    
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

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

current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                              random.choice(list(tetrominoes.values()))['color'])
next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                           random.choice(list(tetrominoes.values()))['color'])

score = 0
level = 1
lines_cleared = 0
level_up_lines = 5
gravity_speed = 30

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
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
                score += 1  # Increment score for soft drop
                if current_tetromino.collision():
                    current_tetromino.move(0, -1)
            if event.key == pygame.K_SPACE:
                drop_distance = hard_drop(current_tetromino)
                score += drop_distance * 2  # Increment score for hard drop
                current_tetromino.move(0, 1)

            if event.key == pygame.K_UP:
                current_tetromino.rotate()
                if current_tetromino.collision():
                    for _ in range(3):
                        current_tetromino.rotate()

    current_tetromino.move(0, 1)
    if current_tetromino.collision():
        current_tetromino.move(0, -1)
        for i in range(len(current_tetromino.shape)):
            for j in range(len(current_tetromino.shape[0])):
                if current_tetromino.shape[i][j]:
                    grid[current_tetromino.y + i][current_tetromino.x + j] = current_tetromino.color
        current_tetromino = next_tetromino
        next_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                   random.choice(list(tetrominoes.values()))['color'])
        if current_tetromino.collision():
            game_over(score, level)
        lines = check_lines()
        lines_cleared += lines
        score += lines * 100
        if lines_cleared >= level_up_lines:
            level += 1
            lines_cleared = 0
            gravity_speed = max(1, gravity_speed - 2)

    draw_text(f'Score: {score}', 36, WHITE, SCREEN_WIDTH - 150, 20)
    draw_text(f'Level: {level}', 36, WHITE, SCREEN_WIDTH - 150, 60)
    draw_text('Next:', 36, WHITE, SCREEN_WIDTH - 150, 140)
    draw_next_tetromino(next_tetromino)

    current_tetromino.draw()
    draw_grid()
    pygame.display.update()
    clock.tick(FPS)
