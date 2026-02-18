import random
from typing import List, Optional

class SudokuGenerator:
    """Generates a fully filled 9x9 Sudoku board that satisfies all Sudoku rules."""
    
    def __init__(self):
        self.size = 9
        self.box_size = 3
    
    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        for c in range(self.size):
            if board[row][c] == num:
                return False
        
        # Check column
        for r in range(self.size):
            if board[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                if board[r][c] == num:
                    return False
        
        return True
    
    def solve(self, board: List[List[int]]) -> bool:
        """Solve the Sudoku board using backtracking."""
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    # Try numbers in random order for variety
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    
    def generate(self) -> List[List[int]]:
        """Generate a new fully filled Sudoku board."""
        # Start with an empty board
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # Fill the board using backtracking
        self.solve(board)
        
        return board
    
    def generate_multiple(self, count: int = 1) -> List[List[List[int]]]:
        """Generate multiple unique Sudoku boards."""
        boards = []
        for _ in range(count):
            boards.append(self.generate())
        return boards




