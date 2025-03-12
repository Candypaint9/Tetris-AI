import pygame, sys
from game import Game

pygame.init()

screen=pygame.display.set_mode((300, 600))
pygame.display.set_caption("TETRIS")

clock=pygame.time.Clock() #to control game FPS and speed

FPS=60 #in-game FPS to remain constant 
bgrd=(95, 17, 144, 1)#background colour

game=Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 700) #auto push current tetromino down every 0.7s

while True:
    for event in pygame.event.get(): #quit game of window closed
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
                game.move_down()
            if event.key==pygame.K_LEFT:
                game.move_left()
            if event.key==pygame.K_RIGHT:
                game.move_right()
            if event.key==pygame.K_UP: 
                game.rotate()
                
        if event.type == GAME_UPDATE:
            game.move_down()        
        
    screen.fill(bgrd)
    game.draw(screen=screen)
    pygame.display.update()
    clock.tick(FPS) 