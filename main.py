import pygame
import random

BOX_SIZE = 10
PADDING = 10
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

BG_COLOR = (10, 14, 18)
GRID_COLOR = (199, 207, 214)

class Piece:
    # Every piece is defined in terms of a 4x4 grid (all rotations)
    pieces = [
        [[5, 6, 7, 8], [3, 7, 11, 15]],      #I
        [[6, 7, 10, 11]],                   #O
        [[7, 8, 10, 11], [3, 7, 8, 12 ]],   #S
        [[6, 7, 11, 12], [3, 6, 7, 10]],     #Z
        [[3, 7, 10, 11], [6, 7, 8, 12], [3, 4, 7, 11], [2, 6, 7, 8]], #J
        [[3, 7, 11, 12], [4, 6, 7, 8], [2, 3, 7, 11], [6, 7, 8, 10]],   #L
        [[6, 7, 8, 11], [3, 7, 8, 11], [3, 6, 7, 8], [3, 6, 7, 11]]  #T
    ]

    colors = [
        (199, 6, 35), #I
        (6, 199, 73), #O
        (3, 44, 252), #S
        (3, 219, 252), #Z
        (125, 6, 199), #J
        (230, 147, 5), #L
        (226, 230, 5)  #T
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pieceType = random.randint(0, len(self.pieces)-1)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.pieces[self.pieceType])

    def getRelativePos(self):
        return self.pieces[self.pieceType][self.rotation]
    

class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = BOX_SIZE * 20
        self.width = BOX_SIZE * 10
        self.xSpawn = 3     #spawn square goes from x=3 to x=7
        self.ySpawn = 0     #spawn square goes from y=0 to y=4
        
        self.score = 0
        self.grid = []
        
        for i in range(20): self.grid.append([0] * 10)

    def spawn(self):
        self.currentPiece = Piece(self.xSpawn, self.ySpawn)

    def rotate(self):
        pass

    def move(self, dir):    #directions = ['u', 'd', 'l', 'r']
        pass

    def place(self):    #to place the block
        pass

    def collision(self):
        pass

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

while True: pass