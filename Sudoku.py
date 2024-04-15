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
BOARD_SIZE = 540  # Size of the game board
WINDOW_SIZE = (BOARD_SIZE * 2, BOARD_SIZE)  # Double the width for buttons on the right
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
            "quit": pygame.Rect(WINDOW_SIZE[0] - 140, 260, 120, 40)
        }
        self.timer = 480 # 8min in seconds
        self.chances = 3
        self.difficulty = "easy"

    def generate_board(self):
        # Generate a solved Sudoku board
        # For simplicity, we just fill in numbers randomly
        for i in range(9):
            for j in range(9):
                self.board[i][j] = random.randint(1, 9)

        # Set the number of empty cells based on the selected difficulty level
        empty_cells = {"easy": 40, "medium": 50, "hard": 60}
        empty_cells_count = empty_cells[self.difficulty]

        # Randomly remove some numbers to create a puzzle
        for _ in range(empty_cells_count):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.board[row][col] = 0

        self.reset_timer() #reset the timer when generating a new board
        self.chances = 3 #Reset the chances counter

    def draw_timer(self):
        timer_text = FONT.render(f"Time: {self.timer // 60:02}:{self.timer % 60:02}", True, BLACK)
        timer_text_rect = timer_text.get_rect(bottomright=(WINDOW_SIZE[0] - 20, WINDOW_SIZE[1] - 20))
        WIN.blit(timer_text, timer_text_rect)
    
    def reset_timer(self):
        self.timer = 480  # Reset the timer to 8 minutes in seconds
    
    def draw_chances(self):
        chance_text = FONT.render(f"Chances left: {self.chances}/3", True, BLACK)
        chance_text_rect = chance_text.get_rect(bottomright=(WINDOW_SIZE[0] - 20, WINDOW_SIZE[1] - 60))  # Adjusted position
        WIN.blit(chance_text, chance_text_rect)

    def draw_board(self):
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

        # Draw buttons for new game, difficulty levels, and quit on the right side
        for button in self.buttons.values():
            pygame.draw.rect(WIN, GRAY, button)

        button_texts = {"start": "Start", "easy": "Easy", "medium": "Medium", "hard": "Hard", "quit": "Quit"}
        for button_name, button_rect in self.buttons.items():
            button_text = FONT.render(button_texts[button_name], True, BLACK)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            WIN.blit(button_text, button_text_rect)

    def draw_selected_cell(self):
        if self.selected:
            rect = pygame.Rect(self.selected[1] * (BOARD_SIZE // 9), self.selected[0] * (BOARD_SIZE // 9), BOARD_SIZE // 9, BOARD_SIZE // 9)
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
    
    def update_timer(self):
        pygame.time.delay(1000)  # Delay for 1 second
        self.timer -= 1
        if self.timer <= 0:
            print("Game Over: Time's up!")
            pygame.quit()
            sys.exit()

    def input_number(self, number):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                if self.is_valid_move(row, col, number):
                    self.board[row][col] = number
                else:
                    self.chances -= 1  # Decrement chances on invalid input
                    if self.chances == 0:
                        print("No more chances left. Generating new game board...")
                        self.generate_board()  # Generate new game board
            else:
                self.chances -= 1  # Decrement chances on invalid input

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
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    sudoku.input_number(event.key - pygame.K_0)

        WIN.fill(WHITE)
        sudoku.draw_board()
        sudoku.draw_selected_cell()
        sudoku.draw_timer()  # Draw the timer
        sudoku.draw_chances()
        sudoku.update_timer()  # Update the timer
        pygame.display.update()

if __name__ == "__main__":
    main()