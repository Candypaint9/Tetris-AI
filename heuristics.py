from tetris import ROWS, COLS

def score(board):
    return board.score

# returns (trueGaps, partialGaps)
def gaps(board):

    def getSurroudings(row, col):
        surroundings = {}
        surroundings['u'] = row == 0 or board.grid[row - 1][col] != 0
        surroundings['d'] = row == ROWS-1 or board.grid[row + 1][col] != 0
        surroundings['l'] = col == 0 or board.grid[row][col - 1] != 0
        surroundings['r'] = col == COLS-1 or board.grid[row][col + 1] != 0

        return surroundings
    

    trueGaps, partialGaps = 0, 0
    for col in range(COLS):
        found = False
        for row in range(ROWS):

            if board.grid[row][col]:
                found = True
                continue

            surroundings = getSurroudings(row, col)

            if (surroundings['u'] or found) and surroundings['d']:
                sum = surroundings['l'] + surroundings['r']
                if sum == 2:
                    trueGaps += 1
                elif sum <= 1:
                    partialGaps += 1

    return trueGaps, partialGaps

def maxHeight(board):

    maxHeight = 0
    for col in range(COLS):
        for row in range(ROWS):
            if board.grid[row][col]:
                maxHeight = max(ROWS - row, maxHeight)
                break
    
    return maxHeight


def bumpiness(board):
    
    heights = [0] * COLS
    for col in range(COLS):
        for row in range(ROWS):
            if board.grid[row][col] != 0:
                heights[col] = ROWS - row
                break 

    bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(COLS - 1))

    return bumpiness

def clearedLines(board):

    return board.prevClearedLines


def getIndividualHeuristics(board):
    
    _gaps = gaps(board)

    parameters = [
        score(board), _gaps[0], _gaps[1], maxHeight(board), bumpiness(board), clearedLines(board)
    ]

    return parameters


def calcHeuristicManually(board, weights):

    _gaps = gaps(board)

    parameters = [
        score(board), _gaps[0], _gaps[1], maxHeight(board), bumpiness(board), clearedLines(board)
    ]

    heuristic = 0
    for i in range(len(parameters)):
        heuristic += weights[i] * parameters[i]

    return heuristic