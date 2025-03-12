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
        [],  # empty
        [[2, 6, 10, 14], [4, 5, 6, 7]],      # I
        [[5, 6, 9, 10]],                     # O
        [[6, 7, 9, 10], [2, 6, 7, 11]],      # S
        [[5, 6, 10, 11], [2, 5, 6, 9]],      # Z
        [[2, 6, 9, 10], [5, 6, 7, 11], [2, 3, 6, 10], [1, 5, 6, 7]],  # J
        [[2, 6, 10, 11], [3, 5, 6, 7], [1, 2, 6, 10], [5, 6, 7, 9]],  # L
        [[2, 5, 6, 7], [2, 5, 6, 10], [5, 6, 7, 10], [2, 6, 7, 10]]   # T
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

    def rotate(self, dir):
        self.rotation = (self.rotation+dir) % len(self.pieces[self.pieceType])

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

        self.currentPiece = Piece(self.xSpawn, self.ySpawn)
        self.nextPiece = Piece(self.xSpawn, self.ySpawn)
        self.heldPiece = None
        self.switched = False

    def debugPrintGrid(self):       #just to print grid :/
        for row in range(ROWS):
                print(self.grid[row])

    def boundsCrossed(self, x, y):
        if x < 0 or y < 0 or x >= COLS or y >= ROWS:
            return True
        return False

    def update(self):   # add in this function to push piece down after certain timer and if cant go down to call place function
        if self.currentPiece is None:
            self.spawn()

        self.clearLine()

        self.fillBoard(window)
        self.draw(window)

    def spawn(self):
        self.currentPiece = self.nextPiece
        self.nextPiece = Piece(self.xSpawn, self.ySpawn)

    def hold(self):
        if self.switched: 
            return

        if self.heldPiece is None:
            self.heldPiece = self.currentPiece
            self.currentPiece = None
        else:
            temp = self.currentPiece
            self.currentPiece = self.heldPiece
            self.heldPiece = temp
        
        #resetting the held piece
        self.heldPiece.x = self.xSpawn
        self.heldPiece.y = self.ySpawn
        self.heldPiece.rotation = 0

        self.switched = True

    def rotateACW(self):
        self.currentPiece.rotate(1)

        if self.collision():
            self.currentPiece.rotate(-1)

    def rotateCW(self):
        self.currentPiece.rotate(-1)

        if self.collision():
            self.currentPiece.rotate(1)

    def moveSide(self, dir):    #directions = -1 or 1   #no moving down only direct placing
        self.currentPiece.x += dir

        if self.collision():
            self.currentPiece.x -= dir
    
    def moveDown(self):
        self.currentPiece.y += 1
        
        if self.collision():
            self.currentPiece.y -= 1
            self.place()

    def place(self):    #to place the block (update the grid for the position of the block and set current block to none)

        maxHeight = 20

        for pos in self.currentPiece.getRelativePos():
            x, y = self.currentPiece.getAbsolutePosition(pos)
            
            if not self.boundsCrossed(x, y):
                self.grid[y][x] = self.currentPiece.pieceType
                maxHeight = min(maxHeight, y)

        self.currentPiece = None
        self.switched = False

        self.score += maxHeight     #Updates the score acc to how far below the piece is palced 

    def collision(self):
        for pos in self.currentPiece.getRelativePos():
            x, y = self.currentPiece.getAbsolutePosition(pos)

            if self.boundsCrossed(x, y) or self.grid[y][x] != 0:
                return True
        return False

    def clearLine(self):    #checks which lines to clear and reduce position of all blocks above it by 1

        linesCleared = 0
        for row in range(ROWS-1, 0, -1):    
            toClear = True
            for col in range(COLS):
                if self.grid[row][col] == 0:
                    toClear = False
            
            if toClear:
                linesCleared += 1
            if linesCleared:
                for col in range(COLS):
                    self.grid[row][col] = self.grid[row-1][col]
            
        #Updating Score
        if linesCleared == 1:
            self.score += 40
        elif linesCleared == 2:
            self.score += 100
        elif linesCleared == 3:
            self.score += 300
        elif linesCleared == 4:
            self.score += 1200

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
            if event.key == pygame.K_UP:
                board.rotateCW()
            if event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                board.moveDown()
            if event.key == pygame.K_c:
                board.hold()
            if event.key == pygame.K_LEFT:
                board.moveSide(-1)
            if event.key == pygame.K_RIGHT:
                board.moveSide(1)

    board.update()
    print(board.score)

    pygame.display.update()
    clock.tick(FPS)