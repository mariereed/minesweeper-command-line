import random
from tabulate import tabulate

def createBeginnerTrueFalseMatrix(height, width, mineCount):
    """ create a 8x8 matrix with 10 true, 54 false randomly placed """

    # use a list comprehension to initialize a 2d array of "false"
    matrix = [[False for x in range(width)] for y in range(height)]

    # now generate random numbers to place the mines, check to make sure not already mined
    while mineCount > 0:
        # generate a random number, one for height and one for width
        randHeight = random.randint(0, height-1)
        randWidth  = random.randint(0, width-1 )

        # check to make sure not already a mine
        # if not, then place it and decrease the counter
        if not matrix[randHeight][randWidth] == True:
            matrix[randHeight][randWidth] = True
            mineCount -= 1

    return matrix


def changeIfValid(newMatrix, x, y):
    if x >= 0 and x < len(newMatrix) and y >= 0 and y < len(newMatrix[0]) and not newMatrix[x][y] == '!':
        newMatrix[x][y] += 1
        return True
    return False


def numberFill(matrix):
    newMatrix = createNewZeroMatrix(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == True:
                newMatrix[i][j] = '!'
                changeIfValid(newMatrix, i  , j-1)
                changeIfValid(newMatrix, i  , j+1)
                changeIfValid(newMatrix, i+1, j  )
                changeIfValid(newMatrix, i+1, j-1)
                changeIfValid(newMatrix, i+1, j+1)
                changeIfValid(newMatrix, i-1, j  )
                changeIfValid(newMatrix, i-1, j-1)
                changeIfValid(newMatrix, i-1, j+1)
                # or...
                # for (di, dj) in [(-1, -1), (0, -1), (1, -1),
                #                  (-1,  0),          (1,  0),
                #                  (-1,  1), (0,  1), (1,  1)]:
                #    changeIfValid(newMatrix, i+di, j+dj)
    return newMatrix


def createNewZeroMatrix(matrix):
    return [[0 for x in y] for y in matrix]

def createNewBlankMatrix(matrix):
    """this will be the matrix that i edit"""
    return [['?' for x in y] for y in matrix]

def tabulateMatrix(matrix):
    return tabulate(matrix, tablefmt="fancy_grid")

def getNextMove(height, width):
    x = int(raw_input('enter a row number 1-{}: '.format(width)))-1
    y = int(raw_input('enter a column number 1-{}: '.format(height)))-1
    return (x, y)

def placeFlag():
    flag = raw_input('place a flag?').lower()
    if flag == 'yes' or flag == 'y':
        return True
    return False

def revealClick(height, width, numberMatrix, blankMatrix):
    x, y = getNextMove(height, width)
    if placeFlag():
        blankMatrix[x][y] = 'F'
        return True
    if numberMatrix[x][y] == '!':
        return False
    elif numberMatrix[x][y] == 0:
        blankMatrix[x][y] = ' '
        # reveal neighbors
        revealNeighbors(numberMatrix, blankMatrix, x, y)
    else:
        blankMatrix[x][y] = numberMatrix[x][y]

    return True

def revealNeighbors(numberMatrix, blankMatrix, x, y):
        revealIfValid(numberMatrix, blankMatrix, x  , y-1)
        revealIfValid(numberMatrix, blankMatrix, x  , y+1)
        revealIfValid(numberMatrix, blankMatrix, x+1, y  )
        revealIfValid(numberMatrix, blankMatrix, x+1, y-1)
        revealIfValid(numberMatrix, blankMatrix, x+1, y+1)
        revealIfValid(numberMatrix, blankMatrix, x-1, y  )
        revealIfValid(numberMatrix, blankMatrix, x-1, y-1)
        revealIfValid(numberMatrix, blankMatrix, x-1, y+1)

def revealIfValid(numberMatrix, blankMatrix, x, y):
    if x >= 0 and x < len(blankMatrix) and y >= 0 and y < len(blankMatrix[0]) and not numberMatrix[x][y] == '!' and blankMatrix[x][y] == '?':
        if numberMatrix[x][y] == 0:
            blankMatrix[x][y] = ' '
            revealNeighbors(numberMatrix, blankMatrix, x, y)
        else:
            blankMatrix[x][y] = numberMatrix[x][y]
        return True
    return False

def revealEndBoard(numberMatrix, currentBoard):
    for i in range(len(numberMatrix)):
        for j in range(len(numberMatrix[i])):
            if numberMatrix[i][j] == '!':
                currentBoard[i][j] = '*'
    return currentBoard

def playGame(height, width, mineCount):
    """ Put everything in here! """

    preMatrix     = createBeginnerTrueFalseMatrix(height, width, mineCount)
    numberMatrix  = numberFill(preMatrix)
    blankMatrix   = createNewBlankMatrix(preMatrix)

    gameRunning   = True

    while gameRunning:
        if revealClick(height, width, numberMatrix, blankMatrix):
            print tabulateMatrix(blankMatrix)
            flagCount = 0
            for array in blankMatrix:
                for item in array:
                    if item == 'F':
                        flagCount += 1
            if mineCount == flagCount:
                gameRunning = False
                print 'You Won!'
        else:
            gameRunning = False
            print 'Game Over, you hit a mine!'
            print tabulateMatrix(revealEndBoard(numberMatrix, blankMatrix))

    doOver = raw_input('Play again? (yes or no): ').lower()
    if doOver == 'yes':
        playGame(8, 8, 10)

playGame(8, 8, 10)
