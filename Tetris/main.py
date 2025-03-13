import pygame, sys
from game import Game

pygame.init()

screen=pygame.display.set_mode((550, 640))
pygame.display.set_caption("TETRIS")

clock=pygame.time.Clock() #to control game FPS and speed

FPS=60 #in-game FPS to remain constant 
bgrd=(95, 17, 144, 1)#background colour
text_col=(255, 255, 255) #text colour
rect_col=(145, 111, 237)

text_font = pygame.font.Font(None, 40)
score_surface = text_font.render("Score", True, text_col)
next_surface = text_font.render("Next", True, text_col)
game_over_surface1 = text_font.render("GAME OVER", True, text_col)
game_over_surface2 = text_font.render("CLICK ON ANY", True, text_col)
game_over_surface3 = text_font.render("KEY TO RESET", True, text_col)



score_rect = pygame.Rect(350, 55, 170, 90)
next_rect = pygame.Rect(350, 215, 170, 180)

game=Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500) #auto push current tetromino down every 0.7s

while True:
    for event in pygame.event.get(): #quit game of window closed
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type==pygame.KEYDOWN:
            if not game.game_ends:
                if event.key==pygame.K_DOWN:
                    game.move_down()
                if event.key==pygame.K_LEFT:
                    game.move_left()
                if event.key==pygame.K_RIGHT:
                    game.move_right()
                if event.key==pygame.K_UP: 
                    game.rotate()

            else:
                game.game_ends=False
                game.restart()
          
        if event.type == GAME_UPDATE and not game.game_ends:
            game.move_down()
              
        
    screen.fill(bgrd)
    screen.blit(score_surface, (400, 20, 50, 50))
    screen.blit(next_surface, (400, 180, 50, 50))

    if game.game_ends == True:
        screen.blit(game_over_surface1, (360, 450, 50, 50))
        screen.blit(game_over_surface2, (340, 485, 50, 50))
        screen.blit(game_over_surface3, (340, 520, 50, 50))
    
    pygame.draw.rect(screen, rect_col, score_rect, 0, 15)
    pygame.draw.rect(screen, rect_col, next_rect, 0, 15)
        
    game.draw(screen=screen)
    pygame.display.update()
    clock.tick(FPS) 