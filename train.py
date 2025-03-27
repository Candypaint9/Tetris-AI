import neat
import pygame
import pickle
import os
import copy
from collections import deque
from tetris import Board, Piece, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH
import heuristics


WINDOW_ROWS = 3
WINDOW_COLS = 8    # To increase rows and columns and to still have everything fit in the screen change tetris.BOX_SIZE

WINDOW_HEIGHT = BOARD_HEIGHT * WINDOW_ROWS
WINDOW_WIDTH = BOARD_WIDTH * WINDOW_COLS

window = None
clock = None
FPS = 240


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


def getBestMoveSequence(board, network):
    
    moveSequences = getAllPossiblePositions(board)

    bestHeuristicVal = float("-inf")
    bestPos = None

    for pos in moveSequences.keys():
        tempBoard = copy.deepcopy(board)
        tempBoard.shouldDraw = False
        tempBoard.currentPiece.x, tempBoard.currentPiece.y, tempBoard.currentPiece.rotation = pos[0], pos[1], pos[2]
        tempBoard.place()
        tempBoard.update(window)

        # uncomment for checking only currentPiece
        # params = heuristics.getIndividualHeuristics(tempBoard, False)
        # heuristicVal = network.activate(params)[0]
        # if heuristicVal > bestHeuristicVal:
        #     bestHeuristicVal = heuristicVal
        #     bestPos = pos

        moveSequencesNext = getAllPossiblePositions(tempBoard)

        for posNext in moveSequencesNext.keys():
            tempBoardNext = copy.deepcopy(tempBoard)
            tempBoardNext.shouldDraw = False
            tempBoardNext.currentPiece.x, tempBoardNext.currentPiece.y, tempBoardNext.currentPiece.rotation = posNext[0], posNext[1], posNext[2]
            tempBoardNext.place()
            tempBoardNext.update(window)

            params = heuristics.getIndividualHeuristics(tempBoardNext, True)
            heuristicVal = network.activate(params)[0]

            if heuristicVal > bestHeuristicVal:
                bestHeuristicVal = heuristicVal
                bestPos = pos

    return moveSequences[bestPos], bestPos


def eval_genomes(genomes, config):

    nets = []
    boards = []
    ge = []

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        
        board = Board((i % WINDOW_COLS) * BOARD_WIDTH, (i % WINDOW_ROWS) * BOARD_HEIGHT, (True if i < WINDOW_COLS * WINDOW_ROWS else False))
        boards.append(board)
        ge.append(genome)

    running = True
    while len(boards) and running:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # remove boards with gameOver
        for i, board in enumerate(boards):
            if board.gameOver:
                nets.pop(i)
                boards.pop(i)
                ge.pop(i)

        for i, (board, net) in enumerate(zip(boards, nets)):

            if i < WINDOW_COLS * WINDOW_ROWS:
                board.shouldDraw = True
                board.x = (i % WINDOW_COLS) * BOARD_WIDTH
                board.y = (i % WINDOW_ROWS) * BOARD_HEIGHT
            else:
                board.shouldDraw = False
            
            bestPos = getBestMoveSequence(board, net)[1]
            board.currentPiece.x, board.currentPiece.y, board.currentPiece.rotation = bestPos[0], bestPos[1], bestPos[2]
            board.place()

            ge[i].fitness = board.score
            
            board.update(window)

        pygame.display.update()
        clock.tick(FPS)


def trainNetwork():

    global window, clock

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill(TILE_COLOR)
    clock = pygame.time.Clock()

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

    try:
        winner = population.run(eval_genomes)
        with open('saved_network.pickle', 'wb') as f:
            pickle.dump(winner, f)
    except KeyboardInterrupt:
        pygame.quit()



# if __name__ == "__main__":
#     trainNetwork()
