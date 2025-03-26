import pygame
import neat
import pickle
import os
from tetris import Board, TILE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, FPS
from train import simulateMove, getBestMoveSequence

window = None
clock = None


def game(network):

    window = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    window.fill(TILE_COLOR)
    clock = pygame.time.Clock()

    board = Board(0, 0)
    moveSequence = []
    moveIndex = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        if moveIndex >= len(moveSequence):
            moveIndex = 0
            moveSequence = getBestMoveSequence(board, network)[0]
        
        simulateMove(board, moveSequence[moveIndex])
        moveIndex += 1
        
        board.update(window)
        pygame.display.update()
        clock.tick(FPS)

    print("Final score reached: ", board.score)


if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

    with open('saved_network.pickle', 'rb') as f:
        genome = pickle.load(f)
    
    network = neat.nn.FeedForwardNetwork.create(genome, config)

    game(network)