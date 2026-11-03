import math
import random
import numpy as np

# Board dimensions for Connect Four
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    """
    Creates an empty Connect Four board (numpy 2D array).

    Returns:
    np.ndarray:
        A 2D numpy array of shape (ROW_COUNT, COLUMN_COUNT) filled with zeros (float).
    """
    # TODO: implement
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    """
    Places a piece (1 or 2) at the specified (row, col) position on the board.

    Parameters:
    board (np.ndarray): The current board, shape (ROW_COUNT, COLUMN_COUNT).
    row (int): The row index where the piece should be placed.
    col (int): The column index where the piece should be placed.
    piece (int): The piece identifier (1 or 2).
    
    Returns:
    None. The 'board' is modified in-place. Do NOT return a new board!
    """
    # TODO: implement
    board[row, col] = piece
    pass


def is_valid_location(board, col):
    """
    Checks if dropping a piece in 'col' is valid (column not full).

    Parameters:
    board (np.ndarray): The current board.
    col (int): The column index to check.

    Returns:
    bool: True if it's valid to drop a piece in this column, False otherwise.
    """
    # TODO: implement
    if np.all(board[:,col] != 0):
        return False
    return True 


def get_next_open_row(board, col):
    """
    Gets the next open row in the given column.

    Parameters:
    board (np.ndarray): The current board.
    col (int): The column index to search.

    Returns:
    int: The row index of the lowest empty cell in this column.
    """
    # TODO: implement
    if is_valid_location(board, col):
        for row in range(ROW_COUNT -1, -1, -1):
            if board[row, col] == 0:
                return row


def winning_move(board, piece):
    """
    Checks if the board state is a winning state for the given piece.

    Parameters:
    board (np.ndarray): The current board.
    piece (int): The piece identifier (1 or 2).

    Returns:
    bool: True if 'piece' has a winning 4 in a row, False otherwise.
    This requires checking horizontally, vertically, and diagonally.
    """
    # TODO: implement
    directions = [
        (0, 1), 
        (1, 0),
        (1, 1), 
        (1, -1)
    ]

    for dr, dc in directions:
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                
                if not(0 <= row +3*dr < ROW_COUNT and 0 <= col+3*dc < COLUMN_COUNT):
                    continue

                if(board[row, col] == piece and board[row, col] == board[row+dr, col+dc] == board[row+2*dr,col +2*dc] == board[row+3*dr, col+3*dc]):
                    return True 

    return False   



def get_valid_locations(board):
    """
    Returns a list of columns that are valid to drop a piece.

    Parameters:
    board (np.ndarray): The current board.

    Returns:
    list of int: The list of column indices that are not full.
    """
    # TODO: implement
    valid = []

    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid.append(col)

    return valid

def is_terminal_node(board):
    """
    Checks if the board is in a terminal state:
      - Either player has won
      - Or no valid moves remain

    Parameters:
    board (np.ndarray): The current board.

    Returns:
    bool: True if the game is over, False otherwise.
    """
    # TODO: implement
    if winning_move(board, 1) or winning_move(board, 2) or not get_valid_locations(board):
        return True 
    return False 


def score_position(board, piece):
    """
    Evaluates the board for the given piece.
    (Already implemented to highlight center-column preference.)

    Parameters:
    board (np.ndarray): The current board.
    piece (int): The piece identifier (1 or 2).

    Returns:
    int: Score favoring the center column. 
         (This can be extended with more advanced heuristics.)
    """
    # This is already done for you; no need to modify
    # The heuristic here scores the center column higher, which means
    # it prefers to play in the center column.
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    return score


def minimax(board, depth, alpha, beta, maximizingPlayer):
    """
    Performs minimax with alpha-beta pruning to choose the best column.

    Parameters:
    board (np.ndarray): The current board.
    depth (int): Depth to which the minimax tree should be explored.
    alpha (float): Alpha for alpha-beta pruning.
    beta (float): Beta for alpha-beta pruning.
    maximizingPlayer (bool): Whether it's the maximizing player's turn.

    Returns:
    tuple:
        - (column (int or None), score (float)):
          column: The chosen column index (None if no moves).
          score: The heuristic score of the board state.
    """
    # TODO: implement
    max_piece = 2
    min_piece = 1

    if is_terminal_node(board):
        if winning_move(board, max_piece):
            return (None, float("inf"))
        elif winning_move(board, min_piece):
            return(None, float("-inf"))
        else:
            return (None, 0)

    if depth == 0:
        return (None, score_position(board, max_piece))

    valid = get_valid_locations(board)

    if maximizingPlayer:
        best_score = float('-inf')
        best_col = None
        for col in valid:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, max_piece)

            new_score = minimax(board, depth -1, alpha, beta, False)[1]
            board[row][col] = 0 

            if new_score > best_score:
                best_score = new_score 
                best_col = col

            alpha = max(alpha, best_score)

            if alpha >= beta:
                break
    else:
        best_score = float('inf')
        best_col = None
        for col in valid:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, min_piece)

            new_score = minimax(board, depth -1, alpha, beta, True)[1]
            board[row][col] = 0 

            if new_score < best_score:
                best_score = new_score 
                best_col = col

            beta = min(beta, best_score)

            if alpha >= beta:
                break
    return (best_col, best_score)


if __name__ == "__main__":
    # Simple debug scenario
    # Example usage: create a board, drop some pieces, then call minimax
    example_board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    print("Debug: Created an empty Connect Four board.\n")
    print(example_board)

    # TODO: Students can test their own logic here once implemented, e.g.:
    # drop_piece(example_board, some_row, some_col, 1)
    # col, score = minimax(example_board, depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True)
    # print("Chosen column:", col, "Score:", score)
    board = create_board()
    print("board created")
    print(get_next_open_row(board, 1), "create_board successful")

    drop_piece(board, 5, 3, 1)
    print("piece was dropped correctly:", board[5,3] == 1)
    print(board)

    print("is third column valid:" , is_valid_location(board, 3))
    print("next row should be right above the last 1:", get_next_open_row(board, 3))

    drop_piece(board, 4, 3, 1)
    drop_piece(board, get_next_open_row(board, 3), 3, 1)
    #test minimax 1
    print(board)

    col, score = minimax(board, 2, float("-inf"), float("inf"), True)
    print("col chosen for piece 2", col)
    print(score)

    drop_piece(board, 5, 2, 2)
    drop_piece(board, 4, 2, 2)
    drop_piece(board, 3, 2, 2)
    print(board)

    col, score = minimax(board, 2, float("-inf"), float("inf"), True)
    print("col chosen for piece 2", col)
    print(score)

    drop_piece(board, get_next_open_row(board, 3), 3, 1)

    print(board)
    print("testing winning yes/no?:", winning_move(board, 1))

    print("list of valid columns", get_valid_locations(board))
    print("terminal?", is_terminal_node(board))


    print("hello")
    