import pygame, sys
from grid import Grid
from tetrominos import *

pygame.init()

screen=pygame.display.set_mode((300, 600))
pygame.display.set_caption("TETRIS")

clock=pygame.time.Clock() #to control game FPS and speed

FPS=60 #in-game FPS to remain constant 
bgrd=(95, 17, 144, 1)#background colour


current_grid=Grid()
current_grid.cur_grid()


while True:
    for event in pygame.event.get(): #quit game of window closed
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(bgrd)
    current_grid.draw_grid(screen=screen)   
    block.draw(screen=screen)     
    pygame.display.update()
    clock.tick(FPS) 