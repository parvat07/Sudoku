import random

def generate_sudoku():
    # Start with an empty grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 grids
    for i in range(0, 9, 3):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = numbers.pop()
    
    # Solve the Sudoku puzzle to create a valid puzzle
    solve_sudoku(grid)
    
    # Remove some numbers to create a puzzle
    remove_count = random.randint(30, 50)
    for _ in range(remove_count):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0  # Empty cell
    
    return grid

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
            
            grid[row][col] = 0  # Backtrack
    
    return False  # No solution

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    
    return True

def print_grid(grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] != 0 else ".", end=" ")
        print()

def play_sudoku():
    print("Welcome to Sudoku!\n")
    sudoku_grid = generate_sudoku()
    print("Here is your Sudoku puzzle:")
    print_grid(sudoku_grid)
    print("\nEnter numbers from 1 to 9 to fill the empty cells.")
    
    while True:
        row = int(input("\nEnter row (1-9): ")) - 1
        col = int(input("Enter column (1-9): ")) - 1
        num = int(input("Enter number (1-9): "))
        
        if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9:
            if sudoku_grid[row][col] == 0:
                if is_valid_move(sudoku_grid, row, col, num):
                    sudoku_grid[row][col] = num
                    print("\nUpdated puzzle:")
                    print_grid(sudoku_grid)
                else:
                    print("\nInvalid move! Try again.")
            else:
                print("\nCell is already filled! Try again.")
        else:
            print("\nInvalid input! Please enter row, column, and number within range.")
        
        if find_empty_cell(sudoku_grid) is None:
            print("\nCongratulations! You solved the Sudoku puzzle!")
            break

if __name__ == "__main__":
    play_sudoku()
