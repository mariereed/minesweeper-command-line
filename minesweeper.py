import random
from tabulate import tabulate


def createBeginnerTrueFalseMatrix(height, width, mineCount):
    """ creates a 8x8 matrix with 10 true, 54 false randomly placed """

    # use a list comprehension to initialize a 2d array of "false"
    matrix = [[False for x in range(width)] for y in range(height)]

    while mineCount > 0:
        # generate a random height and width
        randHeight = random.randint(0, height-1)
        randWidth  = random.randint(0, width-1 )

        # verify not already a mine
        # place and decrease counter
        if matrix[randHeight][randWidth] is not True:
            matrix[randHeight][randWidth] = True
            mineCount -= 1

    return matrix


def isValidTile(matrix, x, y):
    """ validates that x and y are within grid """
    if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]):
        return True
    return False


def changeIfValid(newMatrix, x, y):
    """ validates that x and y are within grid and not a bomb """
    if isValidTile(newMatrix, x, y) and newMatrix[x][y] != '!':
        newMatrix[x][y] += 1
        return True
    return False


def revealIfValid(numberMatrix, blankMatrix, x, y):
    """ checks that x,y is a valid tile, not a bomb, not yet selected and reveals the tile """
    if isValidTile(blankMatrix, x, y) and numberMatrix[x][y] != '!' and blankMatrix[x][y] == '?':
        if numberMatrix[x][y] == 0:
            blankMatrix[x][y] = ' '
            revealNeighbors(numberMatrix, blankMatrix, x, y)
        else:
            blankMatrix[x][y] = numberMatrix[x][y]
        return True
    return False


def numberFill(matrix):
    """ generates bomb neighbor counters for each tile """

    # fetch matrix of zeros
    newMatrix = createNewZeroMatrix(matrix)

    # increase counter for neighbors of bombs
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] is True:
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

    # return the matrix with counters and blanks for bombs
    return newMatrix


def createNewZeroMatrix(matrix):
    """ creates a matrix of zeros """
    return [[0 for x in y] for y in matrix]


def createNewBlankMatrix(matrix):
    """ generates '?' matrix, this is the matrix visible to the user """
    return [['?' for x in y] for y in matrix]


def tabulateMatrix(matrix):
    """ formats any matrix into uniform table """
    return tabulate(matrix, tablefmt="fancy_grid")


def getNextMove(height, width):
    """ retrieves user input for tile selection """
    x = int(raw_input('enter a row number 1-{}: '.format(width)))-1
    y = int(raw_input('enter a column number 1-{}: '.format(height)))-1
    return (x, y)


def placeFlag():
    """ retrieves user input for flag placement """
    flag = raw_input('place a flag?').lower()
    if flag == 'yes' or flag == 'y':
        return True
    return False


def revealClick(height, width, numberMatrix, blankMatrix):
    """ processes the user input to reveal a tile or place a flag """
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
    """ selects the neighbors or a selection for revealing """
    revealIfValid(numberMatrix, blankMatrix, x  , y-1)
    revealIfValid(numberMatrix, blankMatrix, x  , y+1)
    revealIfValid(numberMatrix, blankMatrix, x+1, y  )
    revealIfValid(numberMatrix, blankMatrix, x+1, y-1)
    revealIfValid(numberMatrix, blankMatrix, x+1, y+1)
    revealIfValid(numberMatrix, blankMatrix, x-1, y  )
    revealIfValid(numberMatrix, blankMatrix, x-1, y-1)
    revealIfValid(numberMatrix, blankMatrix, x-1, y+1)


def revealEndBoard(numberMatrix, currentBoard):
    for i in range(len(numberMatrix)):
        for j in range(len(numberMatrix[i])):
            if numberMatrix[i][j] == '!':
                currentBoard[i][j] = '*'
    return currentBoard


def playGame(height, width, mineCount):
    """ Game function sets up matrices, allows tile selection and flagging,
    determines game over, suggests playing again """

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
        playGame(height, width, mineCount)

playGame(8, 8, 10)
