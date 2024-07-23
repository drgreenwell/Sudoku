import tkinter as tk
from tkinter import messagebox
import random
import pygame

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound("error.mp3")

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                bg_color = 'light grey' if (i // 3 + j // 3) % 2 == 0 else 'white'
                cell = tk.Entry(self.root, width=2, font=('Arial', 24), justify='center', bd=1, relief='solid', bg=bg_color)
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.config(validate='key', validatecommand=(self.root.register(self.validate), '%P', '%W'))
                self.cells[i][j] = cell

    def validate(self, P, W):
        if P == "":
            return True
        if P.isdigit() and 1 <= int(P) <= 9:
            if self.is_valid_entry(P, W):
                return True
            else:
                self.play_error_sound()
                return False
        self.play_error_sound()
        return False

    def is_valid_entry(self, P, widget_name):
        row, col = self.get_indices(widget_name)
        num = int(P)
        for i in range(9):
            if self.cells[row][i].get() == str(num) or self.cells[i][col].get() == str(num):
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.cells[i][j].get() == str(num):
                    return False

        return True

    def get_indices(self, widget_name):
        for i in range(9):
            for j in range(9):
                if str(self.cells[i][j]) == widget_name:
                    return i, j
        return None, None

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=3)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_board)
        clear_button.grid(row=9, column=3, columnspan=3)

        generate_button = tk.Button(self.root, text="Generate Puzzle", command=self.generate_puzzle)
        generate_button.grid(row=9, column=6, columnspan=3)

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)

    def get_board(self):
        board = []
        for row in self.cells:
            board_row = []
            for cell in row:
                value = cell.get()
                if value == '':
                    board_row.append(0)
                else:
                    board_row.append(int(value))
            board.append(board_row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[i][j].insert(0, str(board[i][j]))

    def solve(self):
        board = self.get_board()
        if self.sudoku_solver(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error", "No solution exists for this puzzle")

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def sudoku_solver(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.sudoku_solver(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def generate_puzzle(self):
        self.clear_board()  # Clear the board first
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_diagonal_blocks(board)
        self.sudoku_solver(board)
        self.remove_numbers(board, 40)
        self.set_board(board)

    def fill_diagonal_blocks(self, board):
        for i in range(0, 9, 3):
            self.fill_block(board, i, i)

    def fill_block(self, board, row, col):
        num = 1
        for i in range(3):
            for j in range(3):
                while not self.is_safe_fill(board, row + i, col + j, num):
                    num = random.randint(1, 9)
                board[row + i][col + j] = num

    def is_safe_fill(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def remove_numbers(self, board, count):
        while count > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if board[row][col] != 0:
                board[row][col] = 0
                count -= 1

    def play_error_sound(self):
        self.error_sound.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()