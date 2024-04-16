def solve_sudoku(grid):
    empty_cell = find_empty_cell(grid)
    
    if not empty_cell:
        return True  # Puzzle solved
    
    row, col = empty_cell
    
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            if solve_sudoku(grid):
                return True
            
            grid[row][col] = 0  # Backtrack if the solution is not valid
            
    return False  # Puzzle cannot be solved

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(grid, row, col, num):
    # Check if the number is already in the row or column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # Check if the number is already in the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    return True

def print_sudoku(grid):
    for row in grid:
        print(" ".join(str(num) for num in row))

if __name__ == "__main__":
    # Input the partially filled Sudoku puzzle
    puzzle = [
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 2, 0],
        [0, 0, 9, 0, 0, 0, 0, 5, 6],
        [0, 0, 4, 0, 0, 5, 8, 0, 7],
        [3, 6, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [5, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 1, 6, 4, 2]
    ]
    
    if solve_sudoku(puzzle):
        print("Solved Sudoku Puzzle:")
        print_sudoku(puzzle)
    else:
        print("No solution exists for the given Sudoku puzzle.")
