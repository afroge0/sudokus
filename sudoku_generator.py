import copy
import random
from typing import List, Optional

class SudokuGenerator:
    """Generates fully filled 9x9 Sudoku boards and playable puzzles with one solution."""
    
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

    def count_solutions(self, board: List[List[int]], limit: int = 2) -> int:
        """Count how many solutions the puzzle has (up to limit). Uses backtracking on a copy."""
        board_copy = copy.deepcopy(board)
        count = [0]

        def solve_count(b: List[List[int]]) -> None:
            if count[0] >= limit:
                return
            for row in range(self.size):
                for col in range(self.size):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num):
                                b[row][col] = num
                                solve_count(b)
                                if count[0] >= limit:
                                    return
                                b[row][col] = 0
                        return
            count[0] += 1

        solve_count(board_copy)
        return count[0]

    def get_solution(self, board: List[List[int]]) -> Optional[List[List[int]]]:
        """If the board has exactly one solution, return it; otherwise return None."""
        if self.count_solutions(board, limit=2) != 1:
            return None
        board_copy = copy.deepcopy(board)
        self.solve(board_copy)
        return board_copy

    def generate_puzzle(self, clue_count: int = 34) -> tuple:
        """
        Generate a puzzle with exactly one solution.
        Returns (puzzle, solution) so the app can validate user input.
        """
        solution = self.generate()
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        target_removed = 81 - clue_count
        removed = 0
        for (r, c) in cells:
            if removed >= target_removed:
                break
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions(puzzle, limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = original
        return (puzzle, solution)

    def generate_multiple(self, count: int = 1) -> List[List[List[int]]]:
        """Generate multiple unique Sudoku boards."""
        boards = []
        for _ in range(count):
            boards.append(self.generate())
        return boards




