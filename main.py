import pygame
import random

BOX_SIZE = 30
ROWS = 21
COLS = 10
PADDING = 10
WINDOW_HEIGHT = BOX_SIZE * ROWS
WINDOW_WIDTH = BOX_SIZE * COLS
GRID_THICKNESS = 1

FPS = 60

BG_COLOR = (10, 14, 18)
BOARD_BG_COLOR = (28, 7, 61)
GRID_COLOR = (199, 207, 214)


class Piece:
    # Every piece is defined in terms of a 4x4 grid (all rotations)
    pieces = [
        [[4, 5, 6, 7], [2, 6, 10, 14]],      # I
        [[5, 6, 9, 10]],                     # O
        [[6, 7, 9, 10], [2, 6, 7, 11]],      # S
        [[5, 6, 10, 11], [2, 5, 6, 9]],      # Z
        [[2, 6, 9, 10], [5, 6, 7, 11], [2, 3, 6, 10], [1, 5, 6, 7]],  # J
        [[2, 6, 10, 11], [3, 5, 6, 7], [1, 2, 6, 10], [5, 6, 7, 9]],  # L
        [[5, 6, 7, 10], [2, 6, 7, 10], [2, 5, 6, 7], [2, 5, 6, 10]]   # T
    ]

    colors = [
        BOARD_BG_COLOR,
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
        self.pieceType = random.randint(1, len(self.pieces)-1)
        self.color = self.colors[self.pieceType]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.pieces[self.pieceType])

    def undoRotate(self):
        self.rotation = (self.rotation-1) % len(self.pieces[self.pieceType])

    def getRelativePos(self):
        return self.pieces[self.pieceType][self.rotation]
    
    def getAbsolutePosition(self, pos):
        x = pos%4 + self.x
        y = pos//4 + self.y

        return (x, y)
    

class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = BOX_SIZE * ROWS
        self.width = BOX_SIZE * COLS
        self.xSpawn = 3     #spawn square goes from x=3 to x=7
        self.ySpawn = 0     #spawn square goes from y=0 to y=4
        
        self.score = 0
        self.grid = []
        for i in range(ROWS): self.grid.append([0] * COLS)

        self.currentPiece = None

    def debugPrintGrid(self):
        for row in range(ROWS):
                print(self.grid[row])

    def update(self):
        if self.currentPiece is None:
            self.spawn()

        self.fillBoard(window)
        self.draw(window)

    def spawn(self):
        self.currentPiece = Piece(self.xSpawn, self.ySpawn)

    def rotate(self):
        self.currentPiece.rotate()

        if self.collision():
            self.currentPiece.undoRotate()

    def move(self, dir):    #directions = -1 or 1   #no moving down only direct placing
        self.currentPiece.x += dir

        if self.collision():
            self.currentPiece.x -= dir

    def forceDown(self):
        pass

    def place(self):    #to place the block
        pass

    def collision(self):
        for pos in self.currentPiece.getRelativePos():
            x, y = self.currentPiece.getAbsolutePosition(pos)

            if x < 0 or y < 0 or x >= COLS or y >= ROWS or self.grid[x][y] != 0:
                return True
        return False

    def clearLine():    #checks which line to clear and reduced position of all blocks above it by 1
        pass

    def fillBoard(self, window):    #fill only the board with the grid color
        window.fill(GRID_COLOR)

    def draw(self, window): 
        for row in range(ROWS):
            for col in range(COLS):
                cell = pygame.Rect(col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE - GRID_THICKNESS, BOX_SIZE - GRID_THICKNESS)
                cellColor = Piece.colors[self.grid[row][col]]
                pygame.draw.rect(window, cellColor, cell)

        for pos in self.currentPiece.getRelativePos():
            col, row = self.currentPiece.getAbsolutePosition(pos)
            cell = pygame.Rect(col * BOX_SIZE, row * BOX_SIZE, BOX_SIZE - GRID_THICKNESS, BOX_SIZE - GRID_THICKNESS)
            cellColor = self.currentPiece.color
            pygame.draw.rect(window, cellColor, cell)


# The window with BG_COLOR is supposed to contain many boards each with color BOARD_BG_COLOR(helpful during training process to visualize multiple boards at once)

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(BG_COLOR)
clock = pygame.time.Clock()
board = Board(0, 0)


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                board.rotate()
            if event.key == pygame.K_SPACE:
                board.forceDown()
            if event.key == pygame.K_LEFT:
                board.move(-1)
            if event.key == pygame.K_RIGHT:
                board.move(1)

    board.update()

    pygame.display.update()
    clock.tick(FPS)