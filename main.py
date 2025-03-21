import neat
import pygame
from tetris import Board, Piece, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS, COLS, ROWS
import multiprocessing
import os
import pickle
import numpy as np
import copy

import time

POPULATION_SIZE = 200   #make sure to also change this in config.txt
WINDOW_ROWS = 3
WINDOW_COLS = 8    #POPULATION_SIZE // ROWS    # To increase rows and columns and to still have everything fit in the screen change tetris.BOX_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT * WINDOW_ROWS
WINDOW_WIDTH = BOARD_WIDTH * WINDOW_COLS

RUNS_PER_NET = 3


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(TILE_COLOR)
clock = pygame.time.Clock()

#inputs
#(temporary) 21*10 board size + 4 (absolute coordinates of the current piece tiles) + 4 + 4 (relative coordinates of held and next piece)
#outputs
#(rotate left, rotate right, move left, move right, hold, do nothing)


def getFitness(board):
    
    fitness = board.score

    #for each empty space with a block above it give it fitness -= 1000
    mean = 0
    for col in range(COLS):
        found = False
        for row in range(ROWS):
            if found and board.grid[row][col]:
                fitness -= 1000
            if board.grid[row][col]:
                found = True
                mean += ROWS-row
    
    mean //= COLS
    dev = 0
    for col in range(COLS):
        found = False
        for row in range(ROWS):
            if board.grid[row][col]:
                found = True
                dev += abs(mean - row)
                
    dev //= COLS
    fitness -= 500 * dev

    return fitness


def game(genomes, config):

    networks = []
    boards = []
    _genomes = []

    boardIndex = 0
    for genome_id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        _genomes.append(genome)

        board = Board((boardIndex % WINDOW_COLS) * BOARD_WIDTH, (boardIndex % WINDOW_ROWS) * BOARD_HEIGHT, (True if boardIndex < 24 else False))
        boards.append(board)
        boardIndex += 1

    alive = POPULATION_SIZE
    while alive > 0:

        for event in pygame.event.get():
            continue

        alive = 0
        for ind, board in enumerate(boards):

            # creating inputs
            inputs = []
            _grid = copy.deepcopy(board.grid)
            
            for pos in board.currentPiece.getRelativePos():
                col, row = board.currentPiece.getAbsolutePosition(pos)
                if Piece.colors.index(board.currentPiece.color) > 0:
                    _grid[row][col] = 1

            for row in _grid:
                for box in row:
                    inputs.append(min(box, 1))

            if board.heldPiece is None:
                for i in range(4):
                    inputs.append(0)
            else:
                for pos in board.heldPiece.getRelativePos():
                    inputs.append(pos)

            for pos in board.nextPiece.getRelativePos():
                inputs.append(pos)
            
            output = np.argmax(networks[ind].activate(inputs))

            #applying actions
            if output == 0:
                board.rotateCW()
            elif output == 1:
                board.rotateACW()
            elif output == 2:
                board.moveSide(-1)
            elif output == 3:
                board.moveSide(1)
            elif output == 4:
                board.hold()
            
            if board.currentPiece is not None:
                board.moveDown()
            
            alive += int(board.update(window))

            # updating the fitness
            _genomes[ind].fitness = getFitness(board)

            if board.gameOver:
                boards.pop(ind)
                _genomes.pop(ind)
                networks.pop(ind)
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')

    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_file)

    population = neat.Population(config)

    # For stats
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(game)