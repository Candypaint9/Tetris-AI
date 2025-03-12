from grid import Grid
from tetrominos import *
import random

class Game:
    def __init__(self):
        self.grid=Grid()
        self.tetrominos=[LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block=self.get_random_tetromino()
        self.next_block=self.get_random_tetromino()
        self.row_ct=20
        self.col_ct=10
        
    def get_random_tetromino(self): #to generate random tetromino for the game
        if len(self.tetrominos)==0:
            self.tetrominos=[LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block=random.choice(self.tetrominos) #every tetromino can reappear only after all                                              
        self.tetrominos.remove(block)        #other ones have been shown atleast once in the cycle
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if not self.is_within_play():
            self.current_block.move(0, 1)
    
    def move_right(self):
        self.current_block.move(0, 1)
        if not self.is_within_play():
            self.current_block.move(0, -1)
    
    def move_down(self):
        self.current_block.move(1, 0)
        if not self.is_within_play():
            self.current_block.move(-1, 0)#reverting move if out of play bounds

    def is_within_play(self): #checks if every cell of the tetromino is within play area
        cells=self.current_block.get_cell_positions()
        for cell in cells:
            if not self.grid.is_inside(cell.row, cell.col):
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw_grid(screen=screen)
        self.current_block.draw(screen=screen)
        
    
    