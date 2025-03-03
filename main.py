import pygame
import random

BOX_SIZE = 10
PADDING = 10
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200
FPS = 60

BG_COLOR = (10, 14, 18)
BOARD_BG_COLOR = (58, 36, 59)
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

        self.currentPiece = None

    def spawn(self):
        self.currentPiece = Piece(self.xSpawn, self.ySpawn)

    def rotate(self):
        pass

    def move(self, dir):    #directions = -1 or 1   #no moving down only direct placing
        pass

    def forceDown(self):
        pass

    def place(self):    #to place the block
        pass

    def collision(self):
        pass

    def clearLine():    #checks which line to clear and reduced position of all blocks above it by 1
        pass

    def fillBoard(self, window):    #fill only the board with the boardbg color
        pass

    def drawGrid(self, window):     #draw the horizontal and vertical lines
        pass

    def drawPieces(self, window):   #draw the pieces
        pass


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(BG_COLOR)
clock = pygame.time.Clock()
board = Board(0, 0)


running = True

while running:

    if board.currentPiece is None:
        board.spawn()

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
            
    board.fillBoard(window)
    board.drawGrid(window)
    board.drawPieces(window)

    pygame.display.update()
    clock.tick(FPS)