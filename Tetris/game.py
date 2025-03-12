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
        if not self.is_within_play() or not self.allowed_to_move():
            self.current_block.move(0, 1)
    
    def move_right(self):
        self.current_block.move(0, 1)
        if not self.is_within_play() or not self.allowed_to_move():
            self.current_block.move(0, -1)
    
    def move_down(self):
        self.current_block.move(1, 0)
        #self.current_block.move(1, 0)
        if not self.is_within_play() or not self.allowed_to_move():
            self.current_block.move(-1, 0)#reverting move if out of play bounds
            self.fix_block() #fix the position of the block if it hits bottom

    def rotate(self): #rotate the current tetrominp
        self.current_block.rotate()
        if not self.is_within_play() or not self.allowed_to_move():
            self.current_block.undo_rotate() #undo rotation if any cell of rotated state is out of bounds
            
    def fix_block(self):
        cells=self.current_block.get_cell_positions()
        for cell in cells:
            self.grid.grid[cell.row][cell.col]=self.current_block.id
        self.grid.clear_filled_rows_and_shift()
        self.current_block=self.next_block
        self.next_block=self.get_random_tetromino()
        
    def allowed_to_move(self): #if block can make move without any collision
        cells=self.current_block.get_cell_positions()
        for cell in cells:
            if self.grid.grid[cell.row][cell.col]!=0:
                return False
        return True
        
    def is_inside(self, row, col):#checks if a block's cell is within play area
            if row>=0 and row<self.row_ct and col>=0 and col<self.col_ct:
                return True
            return False
    
    def is_within_play(self): #checks if every cell of the tetromino is within play area
        cells=self.current_block.get_cell_positions()
        for cell in cells:
            if not self.is_inside(cell.row, cell.col):
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw_grid(screen=screen)
        self.current_block.draw(screen=screen)
        
    
    