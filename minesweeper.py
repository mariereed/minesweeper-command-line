import random
from tabulate import tabulate


def create_true_false_matrix(height, width, mine_count):
    """ creates a {width}x{height} matrix with {mine_count} true randomly placed, the rest false """

    # use a list comprehension to initialize a 2d array of "false"
    matrix = [[False for x in range(width)] for y in range(height)]

    while mine_count > 0:
        # generate a random height and width
        rand_height = random.randint(0, height-1)
        rand_width  = random.randint(0, width-1 )

        # verify not already a mine
        # place and decrease counter
        if matrix[rand_height][rand_width] is not True:
            matrix[rand_height][rand_width] = True
            mine_count -= 1

    return matrix


def is_valid_tile(matrix, x, y):
    """ validates that x and y are within grid """
    if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]):
        return True
    return False


def change_if_valid(new_matrix, x, y):
    """ validates that x and y are within grid and not a bomb """
    if is_valid_tile(new_matrix, x, y) and new_matrix[x][y] != '!':
        new_matrix[x][y] += 1
        return True
    return False


def reveal_if_valid(answer_matrix, current_board, x, y):
    """ checks that x,y is a valid tile, not a bomb, not yet selected and reveals the tile """
    if is_valid_tile(current_board, x, y) and answer_matrix[x][y] != '!' and current_board[x][y] == '?':
        if answer_matrix[x][y] == 0:
            current_board[x][y] = ' '
            reveal_neighbors(answer_matrix, current_board, x, y)
        else:
            current_board[x][y] = answer_matrix[x][y]
        return True
    return False


def number_fill(matrix):
    """ generates bomb neighbor counters for each tile """

    # fetch matrix of zeros
    new_matrix = create_new_zero_matrix(matrix)

    # increase counter for neighbors of bombs
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] is True:
                new_matrix[i][j] = '!'
                change_if_valid(new_matrix, i  , j-1)
                change_if_valid(new_matrix, i  , j+1)
                change_if_valid(new_matrix, i+1, j  )
                change_if_valid(new_matrix, i+1, j-1)
                change_if_valid(new_matrix, i+1, j+1)
                change_if_valid(new_matrix, i-1, j  )
                change_if_valid(new_matrix, i-1, j-1)
                change_if_valid(new_matrix, i-1, j+1)

    # return the matrix with counters and blanks for bombs
    return new_matrix


def create_new_zero_matrix(matrix):
    """ creates a matrix of zeros """
    return [[0 for x in y] for y in matrix]


def create_new_current_board(matrix):
    """ generates '?' matrix, this is the matrix visible to the user """
    return [['?' for x in y] for y in matrix]


def tabulate_matrix(matrix):
    """ formats any matrix into uniform table """
    return tabulate(matrix, tablefmt="fancy_grid")


def is_number(input):
    try:
        return int(input) - 1
    except ValueError:
        return False


def get_next_move(height, width, answer_matrix):
    """ retrieves user input for tile selection """
    x = is_number(raw_input('enter a row number 1-{}: '.format(width)))
    y = is_number(raw_input('enter a column number 1-{}: '.format(height)))
    if x is not False and y is not False and is_valid_tile(answer_matrix, x, y):
        return x, y
    return False, False


def place_flag():
    """ retrieves user input for flag placement """
    flag = raw_input('place a flag?').lower()
    if flag == 'yes' or flag == 'y':
        return True
    return False


def reveal_click(height, width, answer_matrix, current_board, flag_count):
    """ processes the user input to reveal a tile or place a flag """
    x, y = get_next_move(height, width, answer_matrix)

    if x is not False and y is not False:
        if place_flag():
            current_board[x][y] = 'F'
            flag_count += 1
            return flag_count, True
        elif answer_matrix[x][y] == '!':
            return flag_count, False
        elif answer_matrix[x][y] == 0:
            current_board[x][y] = ' '
            reveal_neighbors(answer_matrix, current_board, x, y)
        else:
            current_board[x][y] = answer_matrix[x][y]
        return flag_count, True
    else:
        print 'Please provide a valid number!'
        return reveal_click(height, width, answer_matrix, current_board, flag_count)


def reveal_neighbors(answer_matrix, current_board, x, y):
    """ selects the neighbors of a selection for revealing """
    reveal_if_valid(answer_matrix, current_board, x  , y-1)
    reveal_if_valid(answer_matrix, current_board, x  , y+1)
    reveal_if_valid(answer_matrix, current_board, x+1, y  )
    reveal_if_valid(answer_matrix, current_board, x+1, y-1)
    reveal_if_valid(answer_matrix, current_board, x+1, y+1)
    reveal_if_valid(answer_matrix, current_board, x-1, y  )
    reveal_if_valid(answer_matrix, current_board, x-1, y-1)
    reveal_if_valid(answer_matrix, current_board, x-1, y+1)


def reveal_winning_board(matrix):
    with_blanks_board = [[' ' if x == 0 else x for x in y] for y in matrix]
    with_flags_board = [['F' if x == '!' else x for x in y] for y in with_blanks_board]

    return with_flags_board


def reveal_end_board(answer_matrix, current_board):
    copy_current_board = current_board
    for i in range(len(answer_matrix)):
        for j in range(len(answer_matrix[i])):
            if answer_matrix[i][j] == '!':
                copy_current_board[i][j] = '*'
    return copy_current_board


def print_instructions():
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


def play_game(height, width, mine_count):
    """ Game function sets up matrices, allows tile selection and flagging,
    determines game over, suggests playing again """

    pre_matrix     = create_true_false_matrix(height, width, mine_count)
    answer_matrix  = number_fill(pre_matrix)
    current_board  = create_new_current_board(pre_matrix)

    game_running   = True
    flag_count     = 0

    print_instructions()
    while game_running:
        flag_count, was_revealed = reveal_click(height, width, answer_matrix, current_board, flag_count)
        if was_revealed:
            print tabulate_matrix(current_board)
            print 'Mines Flagged: {} out of {}'.format(flag_count, mine_count)
            if mine_count == flag_count:
                if reveal_winning_board(answer_matrix) == current_board:
                    game_running = False
                    print 'You Won!'
        else:
            game_running = False
            print 'Game Over, you hit a mine!'
            print tabulate_matrix(reveal_end_board(answer_matrix, current_board))

    doOver = raw_input('Play again? ').lower()
    if doOver == 'yes' or doOver == 'y':
        play_game(height, width, mine_count)

play_game(8, 8, 16)
