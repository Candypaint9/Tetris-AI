import neat
import pygame
from tetris import Board, Piece, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS, COLS, ROWS
import os
import numpy as np
import copy
from collections import deque


import time

POPULATION_SIZE = 24   #make sure to also change this in config.txt
WINDOW_ROWS = 3
WINDOW_COLS = 8    #POPULATION_SIZE // ROWS    # To increase rows and columns and to still have everything fit in the screen change tetris.BOX_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT * WINDOW_ROWS
WINDOW_WIDTH = BOARD_WIDTH * WINDOW_COLS

RUNS_PER_NET = 3


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(TILE_COLOR)
clock = pygame.time.Clock()

""""
inputs
1) score
2) gaps (empty squares with blocks surrounding them)
3) mean height
4) mean deviation of height


outputs: rotate left, rotate right, move left, move right, hold, do nothing
"""


def getFitness(board, weights = [3, -500, -10, 0]):
    
    gaps = 0
    meanHeight = 0.0
    for col in range(COLS):
        found = False
        for row in range(ROWS):
            if found and board.grid[row][col] == 0:
                gaps += 1
            if not found and board.grid[row][col]:
                found = True
                meanHeight += ROWS - row
    meanHeight /= COLS

    heightDev = 0.0
    for col in range(COLS):
        found = False
        for row in range(ROWS):
            if not found and board.grid[row][col]:
                found = True
                heightDev += abs(meanHeight - row)
    heightDev /= COLS

    print(board.score, gaps, meanHeight)

    return weights[0] * board.score + weights[1] * gaps + weights[2] * meanHeight + weights[3] * heightDev


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
            
            inputs = []
            # checking all possible moves and calculating inputs
            

            
            outputs = networks[ind].activate(inputs)
            
            alive += int(board.update(window))

            # updating the fitness
            _genomes[ind].fitness = getFitness(board)

            if board.gameOver:
                boards.pop(ind)
                _genomes.pop(ind)
                networks.pop(ind)
        
        pygame.display.update()
        clock.tick(FPS)


def getAllPossiblePositions(board):

    possible_positions = {}  # Maps (x, y, rotation) -> move sequence
    visited = set()
    
    # Original piece state
    original_x, original_y, original_rotation = board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation
    
    # BFS queue: (x, y, rotation, move_sequence)
    queue = deque([(original_x, original_y, original_rotation, [])])
    visited.add((original_x, original_y, original_rotation))

    while queue:
        x, y, rotation, moves = queue.popleft()

        # Move piece to this state
        board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = x, y, rotation

        # checking left, right
        for dx, move in [(-1, "Left"), (1, "Right")]:
            new_x, new_y, new_rotation = x + dx, y, rotation
            if (new_x, new_y, new_rotation) not in visited:
                board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = new_x, new_y, new_rotation
                if not board.collision():
                    visited.add((new_x, new_y, new_rotation))
                    queue.append((new_x, new_y, new_rotation, moves + [move]))
        
        #checking rotations
        for d_rotation, move in [(1, "RotateCW"), (-1, "RotateACW")]:
            new_x, new_y, new_rotation = x, y, (rotation + d_rotation) % len(Piece.pieces[board.currentPiece.pieceType])
            if (new_x, new_y, new_rotation) not in visited:
                board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = new_x, new_y, new_rotation
                if not board.collision():
                    visited.add((new_x, new_y, new_rotation))
                    queue.append((new_x, new_y, new_rotation, moves + [move]))

        # checking down
        new_x, new_y, new_rotation = x, y+1, rotation
        if (new_x, new_y, new_rotation) not in visited:
            board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = new_x, new_y, new_rotation
            if not board.collision():
                visited.add((new_x, new_y, new_rotation))
                queue.append((new_x, new_y, new_rotation, moves + ["Down"]))
            elif (new_x, new_y, new_rotation) not in possible_positions.keys():
                possible_positions[(new_x, new_y, new_rotation)] = moves

    # Restore original state
    board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = original_x, original_y, original_rotation

    return possible_positions



def simulateMoves(board, moves):
    
    for i, move in enumerate(moves):

        for event in pygame.event.get():
            continue

        if move == 'Down':
            board.moveDown()
        elif move == 'Right':
            board.moveSide(1)
        elif move == 'Left':
            board.moveSide(-1)
        elif move == 'RotateCW':
            board.rotateCW()
        elif move == 'RotateACW':
            board.rotateACW()

        board.update(window)
        pygame.display.update()
        clock.tick(FPS)

    while not board.collision():
        board.currentPiece.y += 1
    board.currentPiece.y -= 1
    board.place()
    
    board.update(window)
    pygame.display.update()
    clock.tick(FPS)


def pureSearch():

    board = Board(0, 0)

    running = True
    while running:

        moveSequences = getAllPossiblePositions(board)

        bestFitness = float("-inf")
        bestSequence = None

        for state in moveSequences.keys():
            tempBoard = copy.deepcopy(board)
            #tempBoard.shouldDraw = False
            simulateMoves(tempBoard, moveSequences[state])

            fitness = getFitness(tempBoard)
            if fitness > bestFitness:
                bestSequence = moveSequences[state]
                bestFitness = fitness

        simulateMoves(board, bestSequence)


if __name__ == "__main__":
    
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')

    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_file)
    
    pureSearch()

    # population = neat.Population(config)

    # # For stats
    # population.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # population.add_reporter(stats)

    # population.run(game)

