import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Set up window
BOARD_SIZE = 500  # Size of the game board
WINDOW_SIZE = (1080, 720)  # Double the width for buttons on the right
WIN = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku")

# Set up fonts
FONT = pygame.font.SysFont(None, 40)

class Sudoku:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.selected = None  # Placeholder for selected cell
        self.buttons = {
            "start": pygame.Rect(WINDOW_SIZE[0] - 140, 20, 120, 40),
            "easy": pygame.Rect(WINDOW_SIZE[0] - 140, 80, 120, 40),
            "medium": pygame.Rect(WINDOW_SIZE[0] - 140, 140, 120, 40),
            "hard": pygame.Rect(WINDOW_SIZE[0] - 140, 200, 120, 40),
            "quit": pygame.Rect(WINDOW_SIZE[0] - 140, 260, 120, 40),
            "solve": pygame.Rect(WINDOW_SIZE[0] - 140, 320, 120, 40),
            "undo": pygame.Rect(WINDOW_SIZE[0] - 140, 380, 120, 40)  # Added undo button
        }

        self.timer = 480  # 8min in seconds
        self.chances = 3
        self.difficulty = "easy"
        self.start_time = pygame.time.get_ticks()

        # Stack to store previous board states for undo functionality
        self.undo_stack = []

    def solve_sudoku(self):
        # Helper function to solve Sudoku using backtracking
        def is_valid(row, col, num):
            # Check if the number can be placed in the given position
            for i in range(9):
                if self.board[row][i] == num or self.board[i][col] == num:
                    return False

            start_row, start_col = (row // 3) * 3, (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    if self.board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(i, j, num):
                                self.board[i][j] = num
                                if solve():
                                    return True
                                self.board[i][j] = 0
                        return False
            return True

        solve()

    def is_solvable(self):
        # Create a copy of the board
        temp_board = [row[:] for row in self.board]

        def is_valid(row, col, num):
            # Check if the number can be placed in the given position
            for i in range(9):
                if temp_board[row][i] == num or temp_board[i][col] == num:
                    return False

            start_row, start_col = (row // 3) * 3, (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    if temp_board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if temp_board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(i, j, num):
                                temp_board[i][j] = num
                                if solve():
                                    return True
                                temp_board[i][j] = 0
                        return False
            return True

        return solve()

    def generate_board(self):
        # Generate a solved Sudoku board
        self.solve_sudoku()

        # Set the number of empty cells based on the selected difficulty level
        empty_cells = {"easy": 40, "medium": 50, "hard": 70}
        empty_cells_count = empty_cells[self.difficulty]

        # Randomly remove some numbers to create a puzzle
        for _ in range(empty_cells_count):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            # Ensure that the cell is not already empty
            while self.board[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            # Temporarily store the cell value
            temp = self.board[row][col]
            # Remove the number from the cell
            self.board[row][col] = 0
            # Check if the puzzle remains solvable after removing the number
            if not self.is_solvable():
                # If not solvable, revert the change and try another cell
                self.board[row][col] = temp

        self.reset_timer()  # reset the timer when generating a new board
        self.chances = 3  # Reset the chances counter

        # Clear undo stack when generating a new board
        self.undo_stack.clear()

    def draw_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert milliseconds to seconds
        remaining_time = max(0, self.timer - elapsed_time)  # Calculate remaining time
        timer_text = FONT.render(f"Time: {remaining_time // 60:02}:{remaining_time % 60:02}", True, BLACK)
        timer_text_rect = timer_text.get_rect(bottomright=(WINDOW_SIZE[0] - 20, WINDOW_SIZE[1] - 20))
        WIN.blit(timer_text, timer_text_rect)

    def reset_timer(self):
        self.start_time = pygame.time.get_ticks()  # Reset the timer to 8 minutes in seconds

    def draw_chances(self):
        chance_text = FONT.render(f"Chances left: {self.chances}/3", True, BLACK)
        chance_text_rect = chance_text.get_rect(bottomright=(WINDOW_SIZE[0] - 20, WINDOW_SIZE[1] - 60))  # Adjusted position
        WIN.blit(chance_text, chance_text_rect)

    def draw_instructions(self):

        instruction_font = pygame.font.SysFont(None, 25)

        instructions = [
            "Instructions:",
            "1. Click on a cell to select it.",
            "2. Press a number key to input a value.",
            "3. Use the buttons on the right to start a game, select difficulty, solve, undo, or quit.",
            "4. When Solve buttons is clicked it will show the answer(need to wait 7 sec for new game)",
            "5. You have three chances to input an incorrect number (only correct number will be shown)."
        ]
        instruction_y = WINDOW_SIZE[1] - len(instructions) * 26 - 10  # Align with bottom of window
        for instruction in instructions:
            text_surface = instruction_font.render(instruction, True, RED)
            text_rect = text_surface.get_rect(bottomleft=(10, instruction_y))
            WIN.blit(text_surface, text_rect)
            instruction_y += 30  # Increase Y-coordinate for the next instruction

    def draw_board(self):

        self.draw_instructions()
        # Draw main box boundaries
        for i in range(1, 3):
            pygame.draw.line(WIN, BLACK, (i * (BOARD_SIZE // 3), 0), (i * (BOARD_SIZE // 3), BOARD_SIZE), 3)
            pygame.draw.line(WIN, BLACK, (0, i * (BOARD_SIZE // 3)), (BOARD_SIZE, i * (BOARD_SIZE // 3)), 3)

        # Draw cell boundaries and numbers
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(j * (BOARD_SIZE // 9), i * (BOARD_SIZE // 9), BOARD_SIZE // 9, BOARD_SIZE // 9)
                pygame.draw.rect(WIN, WHITE, rect, 1)

                if self.board[i][j] != 0:
                    text_surface = FONT.render(str(self.board[i][j]), True, BLACK)
                    text_rect = text_surface.get_rect(center=rect.center)
                    WIN.blit(text_surface, text_rect)

        # Draw horizontal lines for each row
        for i in range(1, 9):
            pygame.draw.line(WIN, GRAY, (0, i * (BOARD_SIZE // 9)), (BOARD_SIZE, i * (BOARD_SIZE // 9)), 1)

        # Draw vertical lines for each column
        for j in range(1, 9):
            pygame.draw.line(WIN, GRAY, (j * (BOARD_SIZE // 9), 0), (j * (BOARD_SIZE // 9), BOARD_SIZE), 1)

        # Draw the top border line
        pygame.draw.line(WIN, BLACK, (0, 0), (BOARD_SIZE, 0), 3)
        # Draw the bottom border line
        pygame.draw.line(WIN, BLACK, (0, BOARD_SIZE), (BOARD_SIZE, BOARD_SIZE), 3)
        # Draw the left border line
        pygame.draw.line(WIN, BLACK, (0, 0), (0, BOARD_SIZE), 3)
        # Draw the right border line
        pygame.draw.line(WIN, BLACK, (BOARD_SIZE, 0), (BOARD_SIZE, BOARD_SIZE), 3)
        # Draw instructions

        # Draw buttons for new game, difficulty levels, undo, solve, and quit on the right side
        for button in self.buttons.values():
            pygame.draw.rect(WIN, GRAY, button)

        button_texts = {"start": "Start", "easy": "Easy", "medium": "Medium", "hard": "Hard",
                        "quit": "Quit", "solve": "Solve", "undo": "Undo"}
        for button_name, button_rect in self.buttons.items():
            button_text = FONT.render(button_texts[button_name], True, BLACK)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            WIN.blit(button_text, button_text_rect)

    def draw_selected_cell(self):
        if self.selected:
            rect = pygame.Rect(self.selected[1] * (BOARD_SIZE // 9), self.selected[0] * (BOARD_SIZE // 9),
                               BOARD_SIZE // 9, BOARD_SIZE // 9)
            pygame.draw.rect(WIN, RED, rect, 3)

    def get_clicked_cell(self, pos):
        row = pos[1] // (BOARD_SIZE // 9)
        col = pos[0] // (BOARD_SIZE // 9)
        if (0 <= row < 9) and (0 <= col < 9):
            return (row, col)
        return None

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.generate_board()

    def input_number(self, number):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                if self.is_valid_move(row, col, number):
                    self.board[row][col] = number
                    # Record the move for undo
                    self.undo_stack.append([row, col, 0])  # '0' indicates the move was placing a number
                else:
                    self.chances -= 1  # Decrement chances on invalid input
                    if self.chances == 0:
                        print("No more chances left. Generating new game board...")
                        self.generate_board()  # Generate new game board
            else:
                print("Cell already contains a number")

    def is_valid_move(self, row, col, number):
        # Check if the number can be placed in the given row and column
        return self.is_valid_row(row, number) and \
               self.is_valid_column(col, number) and \
               self.is_valid_subgrid(row, col, number)

    def is_valid_row(self, row, number):
        # Check if the number is not already in the row
        return number not in self.board[row]

    def is_valid_column(self, col, number):
        # Check if the number is not already in the column
        column = [self.board[i][col] for i in range(9)]
        return number not in column

    def is_valid_subgrid(self, row, col, number):
        # Check if the number is not already in the 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == number:
                    return False
        return True

    def is_puzzle_solved(self):
        # Check if there are any empty cells (zeroes) remaining
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def undo_move(self):
        if self.undo_stack:
            row, col, operation = self.undo_stack.pop()
            if operation == 0:  # If the move was placing a number
                self.board[row][col] = 0

def main():
    sudoku = Sudoku()
    sudoku.generate_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                sudoku.selected = sudoku.get_clicked_cell(pos)
                if sudoku.selected:
                    print("Selected cell:", sudoku.selected)
                for button_name, button_rect in sudoku.buttons.items():
                    if button_rect.collidepoint(pos):
                        if button_name == "start":
                            print("Start button clicked")
                            sudoku.generate_board()  # Generate new game board
                            sudoku.reset_timer()  # Reset the timer
                        elif button_name == "easy":
                            print("Easy button clicked")
                            sudoku.set_difficulty("easy")
                            sudoku.reset_timer()  # Reset the timer
                        elif button_name == "medium":
                            print("Medium button clicked")
                            sudoku.set_difficulty("medium")
                            sudoku.reset_timer()  # Reset the timer
                        elif button_name == "hard":
                            print("Hard button clicked")
                            sudoku.set_difficulty("hard")
                            sudoku.reset_timer()  # Reset the timer
                        elif button_name == "quit":
                            print("Quit button clicked")
                            pygame.quit()
                            sys.exit()
                        elif button_name == "solve":
                            print("Solve button clicked")
                            sudoku.solve_sudoku()
                            sudoku.draw_board()
                        elif button_name == "undo":
                            print("Undo button clicked")
                            sudoku.undo_move()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    sudoku.input_number(event.key - pygame.K_0)

        WIN.fill(WHITE)
        sudoku.draw_board()
        sudoku.draw_selected_cell()
        sudoku.draw_timer()  # Draw the timer
        sudoku.draw_chances()

        pygame.display.update()

        if sudoku.timer <= 0:
            print("Time's up! Generating new game board...")
            sudoku.generate_board()
            sudoku.reset_timer()

        # Check if the puzzle is solved
        if sudoku.is_puzzle_solved():
            print("Congratulations! Puzzle solved. Generating new game board...7 sec more")
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 8000:
                pass
            sudoku.generate_board()

        # Reset timer and chances when the game is over
        if sudoku.timer <= 0 or sudoku.is_puzzle_solved():
            sudoku.reset_timer()
            sudoku.chances = 3

if __name__ == "__main__":
    main()
