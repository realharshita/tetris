import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

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

def check_lines():
    global grid
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                              random.choice(list(tetrominoes.values()))['color'])

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.move_left()
                if current_tetromino.collision():
                    current_tetromino.move_right()
            if event.key == pygame.K_RIGHT:
                current_tetromino.move_right()
                if current_tetromino.collision():
                    current_tetromino.move_left()
            if event.key == pygame.K_DOWN:
                current_tetromino.move_down()
                if current_tetromino.collision():
                    current_tetromino.move_down = False
            if event.key == pygame.K_UP:
                current_tetromino.rotate()
                if current_tetromino.collision():
                    for _ in range(3):
                        current_tetromino.rotate()

    current_tetromino.move_down()
    if current_tetromino.collision():
        current_tetromino.y -= 1
        for i in range(len(current_tetromino.shape)):
            for j in range(len(current_tetromino.shape[0])):
                if current_tetromino.shape[i][j]:
                    grid[current_tetromino.y + i][current_tetromino.x + j] = current_tetromino.color
        current_tetromino = Tetromino(random.choice(list(tetrominoes.values()))['shape'],
                                      random.choice(list(tetrominoes.values()))['color'])
        check_lines()

    current_tetromino.draw()
    pygame.display.update()
    clock.tick(FPS)
