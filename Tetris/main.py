import pygame, sys
from game import Game
from local_state_search_neat import LocalStateSearch  # Add this import

pygame.init()

screen = pygame.display.set_mode((550, 640))
pygame.display.set_caption("TETRIS AI")

clock = pygame.time.Clock()

FPS = 60
bgrd = (95, 17, 144, 1)
text_col = (255, 255, 255)
rect_col = (145, 111, 237)

text_font = pygame.font.Font(None, 40)
score_surface = text_font.render("Score", True, text_col)
next_surface = text_font.render("Next", True, text_col)
game_over_surface1 = text_font.render("GAME OVER", True, text_col)
game_over_surface2 = text_font.render("CLICK ON ANY", True, text_col)
game_over_surface3 = text_font.render("KEY TO RESET", True, text_col)

score_rect = pygame.Rect(350, 55, 170, 90)
next_rect = pygame.Rect(350, 215, 170, 180)

# Replace Game() with LocalStateSearch()
game = LocalStateSearch()

MOVE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(MOVE_UPDATE, 50)  # Visual update timer for smooth animation


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and game.game_ends:
            game.game_ends = False
            game.restart()
          
        if event.type == MOVE_UPDATE and not game.game_ends:
            # Complete the current move sequence
            if not game.make_best_move():
                game.move_down()
                
                
    score_value = text_font.render(str(game.score), True, text_col)
    
    screen.fill(bgrd)
    screen.blit(score_surface, (400, 20, 50, 50))
    screen.blit(next_surface, (400, 180, 50, 50))

    if game.game_ends:
        screen.blit(game_over_surface1, (360, 450, 50, 50))
        screen.blit(game_over_surface2, (340, 485, 50, 50))
        screen.blit(game_over_surface3, (340, 520, 50, 50))
    
    pygame.draw.rect(screen, rect_col, score_rect, 0, 15)
    pygame.draw.rect(screen, rect_col, next_rect, 0, 15)
    screen.blit(score_value, score_value.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    
    game.draw(screen=screen)
    pygame.display.update()
    clock.tick(FPS)