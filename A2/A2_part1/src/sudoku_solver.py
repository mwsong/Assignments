def print_board(board):
    """
    Prints the Sudoku board in a grid format.
    0 indicates an empty cell.

    Parameters:
    board (list[list[int]]): A 9x9 Sudoku board where 0 represents an empty cell.

    Returns:
    None
    """
    for row_idx, row in enumerate(board):
        # Print a horizontal separator every 3 rows (for sub-grids)
        if row_idx % 3 == 0 and row_idx != 0:
            print("- - - - - - - - - - -")

        row_str = ""
        for col_idx, value in enumerate(row):
            # Print a vertical separator every 3 columns (for sub-grids)
            if col_idx % 3 == 0 and col_idx != 0:
                row_str += "| "

            if value == 0:
                row_str += ". "
            else:
                row_str += str(value) + " "
        print(row_str.strip())


def find_empty_cell(board):
    """
    Finds an empty cell (indicated by 0) in the Sudoku board.

    Parameters:
    board (list[list[int]]): A 9x9 Sudoku board where 0 represents an empty cell.

    Returns:
    tuple or None:
        - If there is an empty cell, returns (row_index, col_index).
        - If there are no empty cells, returns None.
    """
    # TODO: implement
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == 0:
                return (row_index, col_index)
    return None


def is_valid(board, row, col, num):
    """
    Checks if placing 'num' at board[row][col] is valid under Sudoku rules:
      1) 'num' is not already in the same row
      2) 'num' is not already in the same column
      3) 'num' is not already in the 3x3 sub-box containing that cell

    Parameters:
    board (list[list[int]]): A 9x9 Sudoku board.
    row (int): Row index of the cell.
    col (int): Column index of the cell.
    num (int): The candidate number to place.

    Returns:
    bool: True if valid, False otherwise.
    """
    # TODO: implement
    for cell in board[row]:
        if cell == num:
            return False 
        
    for r in range(9):
        if board[r][col] == num:
            return False 

    box_r = row//3
    box_c = col//3 

    for r in range(box_r*3, box_r*3 + 3):
        for c in range(box_c*3, box_c*3 +3):
            if board[r][c] == num:
                return False 

    return True
        


def solve_sudoku(board):
    """
    Solves the Sudoku puzzle in 'board' using DFS.

    Parameters:
    board (list[list[int]]): A 9x9 Sudoku board where 0 indicates an empty cell.

    Returns:
    bool:
        - True if the puzzle is solved successfully.
        - False if the puzzle is unsolvable.
    """
    # TODO: implement
    cell = find_empty_cell(board)

    if cell is None:
        return True 

    row, col = cell 

    for num in range(1,10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True 

            board[row][col] = 0

    return False





def is_solved_correctly(board):
    """
    Checks that the board is fully and correctly solved:
    - Each row contains digits 1-9 exactly once
    - Each column contains digits 1-9 exactly once
    - Each 3x3 sub-box contains digits 1-9 exactly once

    Parameters:
    board (list[list[int]]): A 9x9 Sudoku board.

    Returns:
    bool: True if the board is correctly solved, False otherwise.
    """
    # TODO: implement
    for row in board:
        if set(row) != set(range(1,10)):
            return False 

    
    for c in range(9):
        col = []
        for r in range(9):
            col.append(board[r][c])
        if set(col) != set(range(1,10)):
            return False

    for box_r in range(3):
        for box_c in range(3):
            box = []

            for r in range(box_r*3, box_r*3 +3):
                for c in range(box_c*3, box_c*3+3):
                    box.append(board[r][c])

            if set(box) != set(range(1, 10)):
                return False

    return True

if __name__ == "__main__":
    # Example usage / debugging:
    example_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]

    print("Debug: Original board:\n")
    print_board(example_board)
    # TODO: Students can call their solve_sudoku here once implemented and check if they got a correct solution.
    solve_sudoku(example_board)
    print(example_board)