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
        # Initialize the Sudoku board
        self.board = [[0] * 9 for _ in range(9)]  # 9x9 grid initialized with 0s
        self.selected = None  # Placeholder for selected cell
        self.buttons = {
            # Dictionary containing button rectangles for GUI
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
        self.message = []

        # Generate a solved Sudoku board
        self.solve_sudoku()

        # Shuffle rows and columns for variety
        self.shuffle_rows_and_columns()

        # Set the number of empty cells based on the selected difficulty level
        empty_cells = {"easy": 40, "medium": 60, "hard": 80}
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

        # Reset timer and chances counter, and clear undo stack
        self.reset_timer()
        self.chances = 3
        self.undo_stack.clear()

    def solve_sudoku(self):
        # Generate a solved Sudoku puzzle
        def is_valid(row, col, num):
            # Check row, column, and subgrid for validity
            return (
                self.is_valid_row(row, num)
                and self.is_valid_column(col, num)
                and self.is_valid_subgrid(row, col, num)
            )

        def solve():
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        # Try placing numbers 1-9
                        for num in range(1, 10):
                            if is_valid(i, j, num):
                                # If placing 'num' is valid, try to solve recursively
                                self.board[i][j] = num
                                if solve():
                                    return True
                                # Backtrack if no solution found
                                self.board[i][j] = 0
                        return False
            return True

        # Start solving the Sudoku puzzle
        solve()

    def is_valid_row(self, row, num):
        return num not in self.board[row]

    def is_valid_column(self, col, num):
        return num not in [row[col] for row in self.board]

    def is_valid_subgrid(self, row, col, num):
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def is_solvable(self):
        # Check if the generated Sudoku puzzle is solvable
        temp_board = [row[:] for row in self.board]

        def solve(temp_board):
            for i in range(9):
                for j in range(9):
                    if temp_board[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid_row(i, num) and self.is_valid_column(j, num) and self.is_valid_subgrid(
                                i, j, num
                            ):
                                temp_board[i][j] = num
                                if solve(temp_board):
                                    return True
                                temp_board[i][j] = 0
                        return False
            return True

        return solve(temp_board)

    def shuffle_rows_and_columns(self):
        # Shuffle the numbers within each row and column to mix up the puzzle
        for i in range(9):
            random.shuffle(self.board[i])
        self.board = list(map(list, zip(*self.board)))
        for i in range(9):
            random.shuffle(self.board[i])
        self.board = list(map(list, zip(*self.board)))
    
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
            "4. When Solve buttons is clicked it will show the answer(need to wait 2 sec for new board)",
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

        # Draw the border line
        pygame.draw.line(WIN, BLACK, (0, 0), (BOARD_SIZE, 0), 3)
        pygame.draw.line(WIN, BLACK, (0, BOARD_SIZE), (BOARD_SIZE, BOARD_SIZE), 3)
        pygame.draw.line(WIN, BLACK, (0, 0), (0, BOARD_SIZE), 3)
        pygame.draw.line(WIN, BLACK, (BOARD_SIZE, 0), (BOARD_SIZE, BOARD_SIZE), 3)
        

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
            cell_size = BOARD_SIZE // 9
            rect = pygame.Rect(self.selected[1] * cell_size, self.selected[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(WIN, RED, rect, 3)


    def get_clicked_cell(self, pos):
        cell_size = BOARD_SIZE // 9
        row = pos[1] // cell_size
        col = pos[0] // cell_size
        return (row, col) if 0 <= row < 9 and 0 <= col < 9 else None

    
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
                        self.add_message("No more chances left. Generating new game board...", duration = 2000)
                        self.generate_board()  # Generate new game board
                        return
                    self.add_message("Invalid move. Try again.", duration = 2000)
            else:
                self.add_message("Cell already contains a number", duration = 2000)

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
    
    def add_message(self, message, duration):
        expiration_time = pygame.time.get_ticks() + duration  # Calculate expiration time
        self.message.append((message, expiration_time))  # Add message with expiration time

    def draw_messages(self):
    # Draw messages on the screen
        message_font = pygame.font.SysFont(None, 30)
        message_y = 26  # Starting Y-coordinate for the first message
        current_time = pygame.time.get_ticks()
        updated_messages = []
        for message_info in self.message:
            message, expiration_time = message_info
            if expiration_time > current_time:
                message_text = message_font.render(message, True, BLACK)
                message_rect = message_text.get_rect(midtop=(WINDOW_SIZE[0] // 2, message_y))
                WIN.blit(message_text, message_rect)
                message_y += message_rect.height + 10  # Increase Y-coordinate for the next message
                updated_messages.append(message_info)
        self.message = updated_messages  # Update the messages list to remove expired messages

def blink_revealed_numbers(self):
    for i, j in self.revealed_numbers:
        cell_size = BOARD_SIZE // 9
        rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
        pygame.draw.rect(WIN, WHITE, rect)  # Clear the cell
        pygame.display.update(rect)  # Update only the cell


def main():
    sudoku = Sudoku()
    sudoku()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(sudoku, event.pos)
            elif event.type == pygame.KEYDOWN:
                handle_key_press(sudoku, event.key)

        update_display(sudoku)

        handle_game_over(sudoku)

def handle_mouse_click(sudoku, pos):
    sudoku.selected = sudoku.get_clicked_cell(pos)
    
    # { if sudoku.selected:
    #   print("Selected cell:", sudoku.selected)} used for debugging
    
    for button_name, button_rect in sudoku.buttons.items():
        if button_rect.collidepoint(pos):
            handle_button_click(sudoku, button_name)

def handle_button_click(sudoku, button_name):
    if button_name == "start":
        sudoku.generate_board()
        sudoku.reset_timer()
    elif button_name in ["easy", "medium", "hard"]:
        sudoku.set_difficulty(button_name)
        sudoku.reset_timer()
    elif button_name == "quit":
                      # print("Quit button clicked")
        pygame.quit()
        sys.exit()
    elif button_name == "solve":
        sudoku.solve_sudoku()
        sudoku.draw_board()
    elif button_name == "undo":
        sudoku.undo_move()

def handle_key_press(sudoku, key):
    if pygame.K_1 <= key <= pygame.K_9:
        sudoku.input_number(key - pygame.K_0)

def update_display(sudoku):
    WIN.fill(WHITE)
    sudoku.draw_board()
    sudoku.draw_selected_cell()
    sudoku.draw_timer()
    sudoku.draw_chances()
    sudoku.draw_messages()
    pygame.display.update()

def handle_game_over(sudoku):
    if sudoku.timer <= 0:
        sudoku.add_message("Time's up! Generating new game board...", duration = 2000)
        sudoku.generate_board()
        sudoku.reset_timer()

    if sudoku.is_puzzle_solved():
        
        
        sudoku.add_message("Congratulations! Puzzle solved. New Game Board Generating...",duration = 5000)
        sudoku.draw_messages()
        pygame.display.update()
        pygame.time.delay(5000)
        sudoku.generate_board()
        # Wait for 2 seconds before generating a new game board
       
       
        sudoku.reset_timer()

if __name__ == "__main__":
    main()

