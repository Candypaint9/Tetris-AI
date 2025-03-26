import neat
import pygame
import copy
from collections import deque
import os
import pickle

import heuristics
from tetris import Board, Piece, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS, COLS, ROWS

POPULATION_SIZE = 100
WINDOW_ROWS = 3
WINDOW_COLS = 8

WINDOW_HEIGHT = BOARD_HEIGHT * WINDOW_ROWS
WINDOW_WIDTH = BOARD_WIDTH * WINDOW_COLS

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NEAT Tetris")
clock = pygame.time.Clock()

def heuristic(board, weights=[5, -600, -100, -6, -12, 300]):
    return heuristics.calcHeuristic(board, weights)

def getAllPossiblePositions(board):
    possible_positions = {}
    visited = set()
    original_x, original_y, original_rotation = board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation
    queue = deque([(original_x, original_y, original_rotation, [])])
    visited.add((original_x, original_y, original_rotation))

    while queue:
        x, y, rotation, moves = queue.popleft()
        board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = x, y, rotation

        for dx, move in [(-1, "Left"), (1, "Right")]:
            new_x, new_y, new_rotation = x + dx, y, rotation
            if (new_x, new_y, new_rotation) not in visited:
                board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = new_x, new_y, new_rotation
                if not board.collision():
                    visited.add((new_x, new_y, new_rotation))
                    queue.append((new_x, new_y, new_rotation, moves + [move]))
        
        mxRot = len(Piece.pieces[board.currentPiece.pieceType])
        for d_rotation, move in [(1, "RotateACW"), (-1, "RotateCW")]:
            new_rotation = (rotation + d_rotation) % mxRot
            if (x, y, new_rotation) not in visited:
                board.currentPiece.rotation = new_rotation
                if not board.collision():
                    visited.add((x, y, new_rotation))
                    queue.append((x, y, new_rotation, moves + [move]))

        new_x, new_y, new_rotation = x, y + 1, rotation
        if (new_x, new_y, new_rotation) not in visited:
            board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = new_x, new_y, new_rotation
            if not board.collision():
                visited.add((new_x, new_y, new_rotation))
                queue.append((new_x, new_y, new_rotation, moves + ["Down"]))
            elif (x, y, rotation) not in possible_positions:
                possible_positions[(x, y, rotation)] = moves + ["Down"]

    board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = original_x, original_y, original_rotation
    return possible_positions

def getBestMoveSequence(board, network):
    moveSequences = getAllPossiblePositions(board)
    bestHeuristicVal = float("-inf")
    bestSequence = None

    for pos in moveSequences:
        tempBoard = copy.deepcopy(board)
        tempBoard.shouldDraw = False
        tempBoard.currentPiece.x, tempBoard.currentPiece.y, tempBoard.currentPiece.rotation = pos
        tempBoard.place()
        tempBoard.update(window)
        
        params = heuristics.getIndividualHeuristics(tempBoard)
        heuristicVal = network.activate(params)[0]

        if heuristicVal > bestHeuristicVal:
            bestHeuristicVal = heuristicVal
            bestSequence = moveSequences[pos]

    return bestSequence

def simulateMoves(board, moves):
    for move in moves:
        if board.currentPiece is None:
            break
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

def eval_genomes(genomes, config):
    nets = []
    boards = []
    ge = []
    
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        x_pos = (i % WINDOW_COLS) * BOARD_WIDTH
        y_pos = (i // WINDOW_COLS) * BOARD_HEIGHT
        board = Board(x_pos, y_pos)
        boards.append(board)
        ge.append(genome)

    running = True
    while running:
        window.fill(TILE_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        all_done = True
        for i, (board, net) in enumerate(zip(boards, nets)):
            if board.gameOver:
                continue
            all_done = False
            
            best_sequence = getBestMoveSequence(board, net)
            simulateMoves(board, best_sequence)
            ge[i].fitness = board.score
            
            board.update(window)

        pygame.display.update()
        clock.tick(FPS)

        if all_done:
            break

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    try:
        winner = population.run(eval_genomes)
        with open('saved_network', 'rb') as f:
            winner = pickle.load(f)
    except KeyboardInterrupt:
        pygame.quit()