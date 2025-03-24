import neat
import pygame
from tetris import Board, Piece, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS, COLS, ROWS
import os
import numpy as np
import copy
from collections import deque
import heuristics


import time

POPULATION_SIZE = 1   #make sure to also change this in config.txt
WINDOW_ROWS = 1
WINDOW_COLS = 1    #POPULATION_SIZE // ROWS    # To increase rows and columns and to still have everything fit in the screen change tetris.BOX_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT * WINDOW_ROWS
WINDOW_WIDTH = BOARD_WIDTH * WINDOW_COLS


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(TILE_COLOR)
clock = pygame.time.Clock()

""""
inputs
1) score
2) trueGaps
3) partialGaps
4) max height
5) bumpiness
6) lines cleared

outputs: weights
"""


def heuristic(board, weights = [10, -600, -50, -15, -20, 150]):
    
    return heuristics.calcHeuristic(board, weights)


def game(genomes, config):

    networks = []
    boards = []
    _genomes = []

    boardIndex = 0
    for genome_id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        _genomes.append(genome)

        board = Board((boardIndex % WINDOW_COLS) * BOARD_WIDTH, (boardIndex % WINDOW_ROWS) * BOARD_HEIGHT, (True if boardIndex < WINDOW_COLS * WINDOW_ROWS else False))
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
            _genomes[ind].fitness = heuristic(board)

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
        mxRot = len(Piece.pieces[board.currentPiece.pieceType])
        for d_rotation, move in [(1, "RotateACW"), (-1, "RotateCW")]:
            new_x, new_y, new_rotation = x, y, ((rotation + d_rotation) % mxRot + mxRot) % mxRot
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
            elif (x, y, rotation) not in possible_positions.keys():
                possible_positions[(x, y, rotation)] = moves + ["Down"]   # for placing block

    # Restore original state
    board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = original_x, original_y, original_rotation

    return possible_positions


def getBestMoveSequence(board):
    
    moveSequences = getAllPossiblePositions(board)

    bestHeuristic = float("-inf")
    bestSequence = None

    for sequence in moveSequences.keys():
        tempBoard = copy.deepcopy(board)
        tempBoard.shouldDraw = False
        tempBoard.currentPiece.x, tempBoard.currentPiece.y, tempBoard.currentPiece.rotation = sequence[0], sequence[1], sequence[2]
        tempBoard.place()
        tempBoard.update(window)

        fitness = heuristic(tempBoard)
        if fitness > bestHeuristic:
            bestSequence = moveSequences[sequence]
            bestHeuristic = fitness

    return bestSequence



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


def pureSearch():

    board = Board(0, 0)

    running = True
    while running:

        bestSequence = getBestMoveSequence(board)

        simulateMoves(board, bestSequence)
        running = not board.gameOver


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

