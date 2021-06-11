# ex11
# ex11_sudoku.py
# eran_levi

from ex11_backtrack import general_backtracking

FILE_PATH = ''
BOARD_SIZE = 9
FRST_COOR = 0
SCND_COOR = 1


def print_board(board, board_size=9):
    """ prints a sudoku board to the screen
    board should be implemented as a dictionary
    that points from a location to a number {(row,col):num}
    """ 
    for row in range(board_size):
        if(row%3 == 0):
            print('-------------')
        toPrint = ''
        for col in range(board_size):
            if(col%3 == 0):
                toPrint += '|'
            toPrint += str(board[(row,col)])
        toPrint += '|'
        print(toPrint)
    print('-------------')


def load_game(sudoku_file):
    """this function loads a text file of sudoku game into a dictionary.
    :param sudoku_file: A path for text file representation of sudoku game.
    :return board - dictionary representation of sudoku game
    """
    board = {}
    with open(sudoku_file, 'r') as wl:
        lines = wl.readlines()
        for n in range(BOARD_SIZE):
            for m in range(BOARD_SIZE*2):
                board[(n,int(m/2))] = lines[n][m-1]
    return board


def check_board(x, board, *args):
    """checking if input is valid.
    :param x: Tuple represent for location in board (row and column
    coordinates.
    :param board: Dictionary representation for sudoku board.
    :return True if assignment is legal and False otherwise.
    """
    n = str(board[x])
    # checking row
    for i in range(BOARD_SIZE):
        if board[x[FRST_COOR],i] == n and i != x[1]:
            return False
    # checking column
    for j in range(BOARD_SIZE):
        if board[j, x[SCND_COOR]] == n and j != x[0]:
            return False
    # checking sub grid
    row_start = (x[FRST_COOR] // 3) * 3
    col_start = (x[SCND_COOR] // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if board[(i,j)] == n and i != x[1] and j != x[1]:
                return False
    return True


def run_game(sudoku_file, print_mode = False):
    """this function running the sudoku game.
    :param sudoku_file: A path for text file representation of sudoku game.
    :param print_mode: Boolean value.
    :return print_mode which tells if game was solved or not in terms of True
    or False.
    """
    # set_of_assignments is a list of legal assignments
    set_of_assignments = list(range(1,10))
    set_of_assignments = [str(k) for k in set_of_assignments]
    # list_of_items is a list of coordinates of all places in board with zero,
    # which need to get a value
    list_of_items = [k for k,v in sudoku_file.items() if v == '0']
    # index for list_of_items to assign value to
    index = 0
    # dict_items_to_vals is a dictionary of list_of_items with values from
    # set_of_assignments
    dict_items_to_vals = {}
    if general_backtracking(sorted(list_of_items), dict_items_to_vals, index,
                    set_of_assignments, check_board, sudoku_file):
        print_mode = True
    return print_mode


if __name__ == '__main__':
    board = load_game(FILE_PATH)
    if run_game(board):
        print_board(board)
    else:
        print(False)