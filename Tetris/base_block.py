from colors import Colors
from position import Position
import pygame

coloring=Colors()


class Block:
    def __init__(self, id):
        self.id=id
        self.cells={}
        self.cell_size=30
        self.rotated=0
        self.rowoffset=self.coloffset=0
        self.colors=coloring.get_cell_colors()
        
    def move(self, rows, cols):
        self.rowoffset+=rows
        self.coloffset+=cols
        
    def get_cell_positions(self):
        to_update=self.cells[self.rotated]
        updated_positions=[]
        for cell in to_update:
            cell=Position(cell.row+self.rowoffset, cell.col+self.coloffset)
            updated_positions.append(cell)
        return updated_positions

    
    def draw(self, screen):
        to_draw=self.get_cell_positions()
        for cell in to_draw: #Drawing the teromino
            cell_rect=pygame.Rect(cell.col*self.cell_size+1, cell.row*self.cell_size+1, self.cell_size-1, self.cell_size-1)
            pygame.draw.rect(screen, self.colors[self.id], cell_rect)