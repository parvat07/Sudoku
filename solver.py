import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600
CELL_SIZE = 60
GRID_SIZE = 9
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

# Sample Sudoku puzzle (0 represents empty cell)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (GRID_WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_HEIGHT), 2)
        else:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (GRID_WIDTH, i * CELL_SIZE))
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_HEIGHT))

# Function to draw the numbers on the Sudoku grid
def draw_numbers():
    font = pygame.font.Font(None, 50)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] != 0:
                text_surface = font.render(str(puzzle[i][j]), True, BLACK)
                text_rect = text_surface.get_rect(center=((j * CELL_SIZE) + (CELL_SIZE // 2), (i * CELL_SIZE) + (CELL_SIZE // 2)))
                screen.blit(text_surface, text_rect)

# Function to draw the cursor
def draw_cursor(cursor_pos):
    pygame.draw.rect(screen, BLUE, (cursor_pos[1] * CELL_SIZE, cursor_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

# Function to check if the move is valid
def is_valid_move(row, col, num):
    # Check row and column
    for i in range(GRID_SIZE):
        if puzzle[row][i] == num or puzzle[i][col] == num:
            return False
    # Check 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if puzzle[i][j] == num:
                return False
    return True

# Function to solve the puzzle (using backtracking)
def solve_sudoku():
    empty_cell = find_empty_cell()
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(row, col, num):
            puzzle[row][col] = num
            if solve_sudoku():
                return True
            puzzle[row][col] = 0
    return False

# Function to find an empty cell in the puzzle
def find_empty_cell():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

# Main game loop
def main():
    cursor_pos = [0, 0]
    selected_number = None
    solving = False

    while True:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_cursor(cursor_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cursor_pos[1] = (cursor_pos[1] - 1) % GRID_SIZE
                elif event.key == pygame.K_RIGHT:
                    cursor_pos[1] = (cursor_pos[1] + 1) % GRID_SIZE
                elif event.key == pygame.K_UP:
                    cursor_pos[0] = (cursor_pos[0] - 1) % GRID_SIZE
                elif event.key == pygame.K_DOWN:
                    cursor_pos[0] = (cursor_pos[0] + 1) % GRID_SIZE
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    selected_number = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    selected_number = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    selected_number = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    selected_number = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    selected_number = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    selected_number = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    selected_number = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    selected_number = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    selected_number = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    selected_number = None
                    puzzle[cursor_pos[0]][cursor_pos[1]] = 0
                elif event.key == pygame.K_SPACE:
                    solving = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                cursor_pos[1] = mouse_pos[0] // CELL_SIZE
                cursor_pos[0] = mouse_pos[1] // CELL_SIZE

        if selected_number is not None:
            if puzzle[cursor_pos[0]][cursor_pos[1]] == 0:
                puzzle[cursor_pos[0]][cursor_pos[1]] = selected_number

        if solving:
            solve_sudoku()
            solving = False

        pygame.display.update()

if __name__ == "__main__":
    main()
