import pygame
from colors import Colors

coloring=Colors()

class Grid:
    def __init__(self):
        self.row_ct=20
        self.col_ct=10
        self.cell_size=30
        self.grid=[[0 for i in range(self.col_ct)] for j in range(self.row_ct)]
        self.colors=coloring.get_cell_colors()
        
    def cur_grid(self): #to print the current grid state
        for i in range(self.row_ct):
            for j in range(self.col_ct):
                print(self.grid[i][j], end=" ") 
            print()
    

    def draw_grid(self, screen):
        for row in range(self.row_ct):
            for col in range(self.col_ct):
                cell=self.grid[row][col]
                cell_rect=pygame.Rect(col*self.cell_size+1, row*self.cell_size+1,  #+1 and -1 to draw the grid lines aswell
                                      self.cell_size-1, self. cell_size-1) #Populating the game grid with cells
                pygame.draw.rect(screen, self.colors[cell], cell_rect)