import neat
import pygame
from tetris import Board, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS

POPULATION_SIZE = 24    
ROWS = 3
COLS = POPULATION_SIZE // ROWS    # To increase rows and columns and to still have everything fit in the screen change tetris.BOX_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT * ROWS
WINDOW_WIDTH = BOARD_WIDTH * COLS


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(TILE_COLOR)
clock = pygame.time.Clock()

boards = []

#initialize population of boards
for i in range(ROWS):
    for j in range(COLS):
        boards.append(Board(BOARD_WIDTH * j, BOARD_HEIGHT * i))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for board in boards:
        board.update(window)
        
    pygame.display.update()
    clock.tick(FPS)
