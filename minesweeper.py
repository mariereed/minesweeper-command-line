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


def isNumber(input):
    try:
        return int(input) - 1
    except ValueError:
        return False


def getNextMove(height, width, numberMatrix):
    """ retrieves user input for tile selection """
    x = isNumber(raw_input('enter a row number 1-{}: '.format(width)))
    y = isNumber(raw_input('enter a column number 1-{}: '.format(height)))
    if x is not False and y is not False and isValidTile(numberMatrix, x, y):
        return x, y
    return False, False


def placeFlag():
    """ retrieves user input for flag placement """
    flag = raw_input('place a flag?').lower()
    if flag == 'yes' or flag == 'y':
        return True
    return False


def revealClick(height, width, numberMatrix, blankMatrix, flagCount):
    """ processes the user input to reveal a tile or place a flag """
    x, y = getNextMove(height, width, numberMatrix)

    if x is not False and y is not False:
        if placeFlag():
            blankMatrix[x][y] = 'F'
            flagCount += 1
            return flagCount, True
        elif numberMatrix[x][y] == '!':
            return flagCount, False
        elif numberMatrix[x][y] == 0:
            blankMatrix[x][y] = ' '
            revealNeighbors(numberMatrix, blankMatrix, x, y)
        else:
            blankMatrix[x][y] = numberMatrix[x][y]
        return flagCount, True
    else:
        print 'Please provide a valid number!'
        return revealClick(height, width, numberMatrix, blankMatrix, flagCount)


def revealNeighbors(numberMatrix, blankMatrix, x, y):
    """ selects the neighbors of a selection for revealing """
    revealIfValid(numberMatrix, blankMatrix, x  , y-1)
    revealIfValid(numberMatrix, blankMatrix, x  , y+1)
    revealIfValid(numberMatrix, blankMatrix, x+1, y  )
    revealIfValid(numberMatrix, blankMatrix, x+1, y-1)
    revealIfValid(numberMatrix, blankMatrix, x+1, y+1)
    revealIfValid(numberMatrix, blankMatrix, x-1, y  )
    revealIfValid(numberMatrix, blankMatrix, x-1, y-1)
    revealIfValid(numberMatrix, blankMatrix, x-1, y+1)


def revealWinningBoard(matrix):
    withBlanksBoard = [[' ' if x == 0 else x for x in y] for y in matrix]
    withFlagsBoard = [['F' if x == '!' else x for x in y] for y in withBlanksBoard]

    return withFlagsBoard

def revealEndBoard(numberMatrix, currentBoard):
    copyCurrentBoard = currentBoard
    for i in range(len(numberMatrix)):
        for j in range(len(numberMatrix[i])):
            if numberMatrix[i][j] == '!':
                copyCurrentBoard[i][j] = '*'
    return copyCurrentBoard


def printInstructions():
    print
    print 'Welcome to Minesweeper!'
    print
    print 'To Play:'
    print 'When prompted provide a row and column number for the tile that you would like to select.'
    print 'You must select a number that fits within the range of the array.'
    print "When asked if you want to place a flag, responding 'y' or 'yes' will place a flag."
    print 'Any other keystroke will instead select the tile, revealing its value.'
    print
    print 'To Win:'
    print 'You must place flags on all the mines and reveal all other tiles.'
    print

def playGame(height, width, mineCount):
    """ Game function sets up matrices, allows tile selection and flagging,
    determines game over, suggests playing again """

    preMatrix     = createBeginnerTrueFalseMatrix(height, width, mineCount)
    numberMatrix  = numberFill(preMatrix)
    blankMatrix   = createNewBlankMatrix(preMatrix)

    gameRunning   = True
    flagCount     = 0

    printInstructions()
    while gameRunning:
        flagCount, wasRevealed = revealClick(height, width, numberMatrix, blankMatrix, flagCount)
        if wasRevealed:
            print tabulateMatrix(blankMatrix)
            print 'Mines Flagged: {} out of {}'.format(flagCount, mineCount)
            if mineCount == flagCount:
                if revealWinningBoard(numberMatrix) == blankMatrix:
                    gameRunning = False
                    print 'You Won!'
        else:
            gameRunning = False
            print 'Game Over, you hit a mine!'
            print tabulateMatrix(revealEndBoard(numberMatrix, blankMatrix))

    doOver = raw_input('Play again? ').lower()
    if doOver == 'yes' or doOver == 'y':
        playGame(height, width, mineCount)

playGame(4, 4, 5)
