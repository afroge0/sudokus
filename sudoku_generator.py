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

    def _ineq_valid(self, board, row, col, num, h_signs, v_signs) -> bool:
        """Check num at (row,col) satisfies all inequality constraints with already-placed neighbours."""
        # Left neighbour
        if col > 0 and board[row][col - 1] != 0:
            sign, left = h_signs[row][col - 1], board[row][col - 1]
            if sign == '<' and not (left < num): return False
            if sign == '>' and not (left > num): return False
        # Right neighbour
        if col < 8 and board[row][col + 1] != 0:
            sign, right = h_signs[row][col], board[row][col + 1]
            if sign == '<' and not (num < right): return False
            if sign == '>' and not (num > right): return False
        # Top neighbour
        if row > 0 and board[row - 1][col] != 0:
            sign, top = v_signs[row - 1][col], board[row - 1][col]
            if sign == '<' and not (top < num): return False
            if sign == '>' and not (top > num): return False
        # Bottom neighbour
        if row < 8 and board[row + 1][col] != 0:
            sign, bottom = v_signs[row][col], board[row + 1][col]
            if sign == '<' and not (num < bottom): return False
            if sign == '>' and not (num > bottom): return False
        return True

    def count_solutions_gt(self, board, h_signs, v_signs, limit: int = 2) -> int:
        """Count solutions satisfying both sudoku rules and all inequality constraints."""
        board_copy = copy.deepcopy(board)
        count = [0]

        def solve_count(b):
            if count[0] >= limit:
                return
            for row in range(self.size):
                for col in range(self.size):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num) and \
                               self._ineq_valid(b, row, col, num, h_signs, v_signs):
                                b[row][col] = num
                                solve_count(b)
                                if count[0] >= limit:
                                    return
                                b[row][col] = 0
                        return
            count[0] += 1

        solve_count(board_copy)
        return count[0]

    def generate_puzzle_gt(self, target_clues: int = 20) -> tuple:
        """
        Generate a Greater Than puzzle uniquely solvable using sudoku rules + inequalities.
        Removes far more digits than a plain sudoku puzzle since inequalities constrain heavily.
        Returns (puzzle, solution, h_signs, v_signs).
        """
        solution = self.generate()

        h_signs = [
            ['<' if solution[r][c] < solution[r][c + 1] else '>' for c in range(8)]
            for r in range(9)
        ]
        v_signs = [
            ['<' if solution[r][c] < solution[r + 1][c] else '>' for c in range(9)]
            for r in range(8)
        ]

        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        for (r, c) in cells:
            if sum(v != 0 for row in puzzle for v in row) <= target_clues:
                break
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions_gt(puzzle, h_signs, v_signs, limit=2) != 1:
                puzzle[r][c] = original

        return (puzzle, solution, h_signs, v_signs)

    def _consec_valid(self, board, row, col, num, h_consec, v_consec) -> bool:
        """Check num at (row,col) satisfies all consecutive constraints with already-placed neighbours."""
        if col > 0 and board[row][col - 1] != 0:
            if (abs(num - board[row][col - 1]) == 1) != h_consec[row][col - 1]:
                return False
        if col < 8 and board[row][col + 1] != 0:
            if (abs(num - board[row][col + 1]) == 1) != h_consec[row][col]:
                return False
        if row > 0 and board[row - 1][col] != 0:
            if (abs(num - board[row - 1][col]) == 1) != v_consec[row - 1][col]:
                return False
        if row < 8 and board[row + 1][col] != 0:
            if (abs(num - board[row + 1][col]) == 1) != v_consec[row][col]:
                return False
        return True

    def count_solutions_consec(self, board, h_consec, v_consec, limit: int = 2) -> int:
        """Count solutions satisfying both sudoku rules and all consecutive constraints."""
        board_copy = copy.deepcopy(board)
        count = [0]

        def solve_count(b):
            if count[0] >= limit:
                return
            for row in range(self.size):
                for col in range(self.size):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num) and \
                               self._consec_valid(b, row, col, num, h_consec, v_consec):
                                b[row][col] = num
                                solve_count(b)
                                if count[0] >= limit:
                                    return
                                b[row][col] = 0
                        return
            count[0] += 1

        solve_count(board_copy)
        return count[0]

    def generate_puzzle_consec(self, target_clues: int = 20) -> tuple:
        """
        Generate a Consecutive Sudoku puzzle uniquely solvable via sudoku rules + consecutive markers.
        h_consec[r][c] = True if solution[r][c] and solution[r][c+1] are consecutive (|a-b|=1).
        v_consec[r][c] = True if solution[r][c] and solution[r+1][c] are consecutive.
        Returns (puzzle, solution, h_consec, v_consec).
        """
        solution = self.generate()
        h_consec = [[abs(solution[r][c] - solution[r][c + 1]) == 1 for c in range(8)] for r in range(9)]
        v_consec = [[abs(solution[r][c] - solution[r + 1][c]) == 1 for c in range(9)] for r in range(8)]
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        for (r, c) in cells:
            if sum(v != 0 for row in puzzle for v in row) <= target_clues:
                break
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions_consec(puzzle, h_consec, v_consec, limit=2) != 1:
                puzzle[r][c] = original
        return (puzzle, solution, h_consec, v_consec)

    def _n2n_valid(self, board, row, col, num, row_clues, col_clues) -> bool:
        """Check if placing num at (row, col) is consistent with Next-to-Nine clues."""
        rc = set(row_clues[row])
        cc = set(col_clues[col])
        if num == 9:
            # Row: clue size must match expected neighbor count (1 if edge, 2 otherwise)
            if len(rc) != (1 if col in (0, 8) else 2): return False
            if col > 0 and board[row][col-1] != 0 and board[row][col-1] not in rc: return False
            if col < 8 and board[row][col+1] != 0 and board[row][col+1] not in rc: return False
            # Col: same logic
            if len(cc) != (1 if row in (0, 8) else 2): return False
            if row > 0 and board[row-1][col] != 0 and board[row-1][col] not in cc: return False
            if row < 8 and board[row+1][col] != 0 and board[row+1][col] not in cc: return False
        else:
            # If 9 is already placed in this row, check adjacency
            for j in range(self.size):
                if board[row][j] == 9 and abs(col - j) == 1:
                    if num not in rc: return False
                    break
            # If 9 is already placed in this col, check adjacency
            for i in range(self.size):
                if board[i][col] == 9 and abs(row - i) == 1:
                    if num not in cc: return False
                    break
        return True

    def count_solutions_n2n(self, board, row_clues, col_clues, limit: int = 2) -> int:
        """Two-phase solver for N2N uniqueness checking.
        Phase 1: Place all 9s using permutation backtracking (most constrained digit first).
        Phase 2: Fill remaining cells with MRV + N2N forward checking.
        """
        board_copy = copy.deepcopy(board)
        count = [0]

        # Identify which rows already have 9 placed
        nine_placed = {}   # row -> col
        used_cols = set()
        for r in range(9):
            for c in range(9):
                if board_copy[r][c] == 9:
                    nine_placed[r] = c
                    used_cols.add(c)
                    break
        rows_without_nine = [r for r in range(9) if r not in nine_placed]

        def phase2(b):
            """Fill non-9 cells with MRV + N2N pruning."""
            if count[0] >= limit:
                return
            best_r, best_c, best_opts = -1, -1, None
            best_n = 10
            for row in range(9):
                for col in range(9):
                    if b[row][col] == 0:
                        opts = [n for n in range(1, 10)
                                if self.is_valid(b, row, col, n) and
                                   self._n2n_valid(b, row, col, n, row_clues, col_clues)]
                        if not opts:
                            return
                        if len(opts) < best_n:
                            best_n, best_r, best_c, best_opts = len(opts), row, col, opts
                            if best_n == 1:
                                break
                if best_n == 1:
                    break
            if best_r == -1:
                count[0] += 1
                return
            for num in best_opts:
                b[best_r][best_c] = num
                phase2(b)
                if count[0] >= limit:
                    return
                b[best_r][best_c] = 0

        def phase1(idx, b, used):
            """Place 9s for rows_without_nine[idx:]."""
            if count[0] >= limit:
                return
            if idx == len(rows_without_nine):
                phase2(b)
                return
            r = rows_without_nine[idx]
            rc = set(row_clues[r])
            # Clue size tells us edge vs interior
            candidates = [0, 8] if len(rc) == 1 else list(range(1, 8))
            for c in candidates:
                if c in used or b[r][c] != 0:
                    continue
                cc = set(col_clues[c])
                # Column clue size must match row position
                if len(cc) != (1 if r in (0, 8) else 2):
                    continue
                if not self.is_valid(b, r, c, 9):
                    continue
                # Row neighbours (if placed) must be in clue
                if c > 0 and b[r][c-1] != 0 and b[r][c-1] not in rc:
                    continue
                if c < 8 and b[r][c+1] != 0 and b[r][c+1] not in rc:
                    continue
                # Col neighbours (if placed) must be in col clue
                if r > 0 and b[r-1][c] != 0 and b[r-1][c] not in cc:
                    continue
                if r < 8 and b[r+1][c] != 0 and b[r+1][c] not in cc:
                    continue
                b[r][c] = 9
                used.add(c)
                phase1(idx + 1, b, used)
                if count[0] >= limit:
                    return
                b[r][c] = 0
                used.discard(c)

        phase1(0, board_copy, used_cols.copy())
        return count[0]

    def generate_puzzle_n2n(self) -> tuple:
        """
        Generate a Next-to-Nine puzzle.
        row_clues[r]: sorted digits adjacent to 9 in row r (1 digit if 9 is at edge, else 2).
        col_clues[c]: sorted digits adjacent to 9 in col c.
        Returns (puzzle, solution, row_clues, col_clues).
        """
        solution = self.generate()
        row_clues = []
        for r in range(9):
            pos = solution[r].index(9)
            nbrs = []
            if pos > 0: nbrs.append(solution[r][pos - 1])
            if pos < 8: nbrs.append(solution[r][pos + 1])
            row_clues.append(sorted(nbrs))
        col_clues = []
        for c in range(9):
            col_vals = [solution[r][c] for r in range(9)]
            pos = col_vals.index(9)
            nbrs = []
            if pos > 0: nbrs.append(col_vals[pos - 1])
            if pos < 8: nbrs.append(col_vals[pos + 1])
            col_clues.append(sorted(nbrs))

        # Remove as many digit clues as possible while keeping a unique solution
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        for (r, c) in cells:
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions_n2n(puzzle, row_clues, col_clues, limit=2) != 1:
                puzzle[r][c] = original
        return (puzzle, solution, row_clues, col_clues)

    def _corner_valid(self, board, row, col, num, corner_clues) -> bool:
        """Check if placing num at (row, col) is consistent with all relevant corner clues."""
        for cr in (row - 1, row):
            if cr < 0 or cr > 7:
                continue
            for cc in (col - 1, col):
                if cc < 0 or cc > 7:
                    continue
                key = f"{cr},{cc}"
                if key not in corner_clues:
                    continue
                clue = corner_clues[key][:]
                if num not in clue:
                    return False
                corner_cells = [(cr, cc), (cr, cc + 1), (cr + 1, cc), (cr + 1, cc + 1)]
                remaining = clue[:]
                for d in [board[r2][c2] for r2, c2 in corner_cells
                          if (r2, c2) != (row, col) and board[r2][c2] != 0] + [num]:
                    if d in remaining:
                        remaining.remove(d)
                    else:
                        return False
        return True

    def count_solutions_corner(self, board, corner_clues, limit: int = 2) -> int:
        """Count solutions satisfying sudoku rules + corner clue constraints."""
        board_copy = copy.deepcopy(board)
        count = [0]

        def solve_count(b):
            if count[0] >= limit:
                return
            for row in range(self.size):
                for col in range(self.size):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num) and \
                               self._corner_valid(b, row, col, num, corner_clues):
                                b[row][col] = num
                                solve_count(b)
                                if count[0] >= limit:
                                    return
                                b[row][col] = 0
                        return
            count[0] += 1

        solve_count(board_copy)
        return count[0]

    def generate_puzzle_corner(self, n_corners: int = 20, target_clues: int = 8) -> tuple:
        """
        Generate a Quad Clues puzzle.
        At n_corners intersections, the 4 digits of the surrounding cells are revealed.
        Returns (puzzle, solution, corner_clues) where corner_clues is {"cr,cc": [d1,d2,d3,d4]}.
        """
        solution = self.generate()

        all_corners = [(r, c) for r in range(8) for c in range(8)]
        random.shuffle(all_corners)

        corner_clues = {}
        for cr, cc in all_corners[:n_corners]:
            corner_clues[f"{cr},{cc}"] = sorted([
                solution[cr][cc], solution[cr][cc + 1],
                solution[cr + 1][cc], solution[cr + 1][cc + 1],
            ])

        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        for (r, c) in cells:
            if sum(v != 0 for row in puzzle for v in row) <= target_clues:
                break
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions_corner(puzzle, corner_clues, limit=2) != 1:
                puzzle[r][c] = original

        return (puzzle, solution, corner_clues)

    def _thermo_valid(self, board, row, col, num, thermos) -> bool:
        """Check if placing num at (row, col) satisfies all thermometer constraints."""
        for thermo in thermos:
            for idx, (r, c) in enumerate(thermo):
                if r != row or c != col:
                    continue
                L = len(thermo)
                lo = idx + 1
                hi = 9 - (L - 1 - idx)
                if num < lo or num > hi:
                    return False
                for prev_idx in range(idx):
                    pr, pc = thermo[prev_idx]
                    v = board[pr][pc]
                    if v != 0 and v >= num:
                        return False
                for next_idx in range(idx + 1, L):
                    nr, nc = thermo[next_idx]
                    v = board[nr][nc]
                    if v != 0 and v <= num:
                        return False
        return True

    def count_solutions_thermo(self, board, thermos, limit: int = 2) -> int:
        """Count solutions satisfying sudoku rules + thermometer constraints."""
        board_copy = copy.deepcopy(board)
        count = [0]

        def solve_count(b):
            if count[0] >= limit:
                return
            for row in range(self.size):
                for col in range(self.size):
                    if b[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(b, row, col, num) and \
                               self._thermo_valid(b, row, col, num, thermos):
                                b[row][col] = num
                                solve_count(b)
                                if count[0] >= limit:
                                    return
                                b[row][col] = 0
                        return
            count[0] += 1

        solve_count(board_copy)
        return count[0]

    def _generate_thermos(self, solution, n_thermos=7, length=5):
        """Generate non-overlapping thermometer paths with strictly increasing solution values."""
        used_cells = set()
        thermos = []
        all_cells = [(r, c) for r in range(9) for c in range(9)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        attempts = 0

        while len(thermos) < n_thermos and attempts < 3000:
            attempts += 1
            start = random.choice(all_cells)
            if start in used_cells:
                continue
            path = [start]
            current = start

            while len(path) < length:
                val = solution[current[0]][current[1]]
                neighbors = [
                    (current[0] + dr, current[1] + dc)
                    for dr, dc in directions
                    if 0 <= current[0] + dr < 9 and 0 <= current[1] + dc < 9
                    and solution[current[0] + dr][current[1] + dc] > val
                    and (current[0] + dr, current[1] + dc) not in used_cells
                    and (current[0] + dr, current[1] + dc) not in path
                ]
                if not neighbors:
                    break
                current = random.choice(neighbors)
                path.append(current)

            if len(path) == length and not any(cell in used_cells for cell in path):
                thermos.append(path)
                used_cells.update(path)

        return thermos

    def generate_puzzle_thermo(self, n_thermos=7, target_clues=20) -> tuple:
        """
        Generate a Thermometer Sudoku puzzle.
        Each thermometer is a path of 5 cells where digits increase strictly from bulb to tip.
        Returns (puzzle, solution, thermos) where thermos is [[[r,c],...], ...].
        """
        solution = self.generate()
        thermos = self._generate_thermos(solution, n_thermos=n_thermos, length=5)
        thermos_serial = [[[r, c] for (r, c) in thermo] for thermo in thermos]

        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)

        for (r, c) in cells:
            if sum(v != 0 for row in puzzle for v in row) <= target_clues:
                break
            original = puzzle[r][c]
            puzzle[r][c] = 0
            if self.count_solutions_thermo(puzzle, thermos, limit=2) != 1:
                puzzle[r][c] = original

        return (puzzle, solution, thermos_serial)

    def generate_multiple(self, count: int = 1) -> List[List[List[int]]]:
        """Generate multiple unique Sudoku boards."""
        boards = []
        for _ in range(count):
            boards.append(self.generate())
        return boards




