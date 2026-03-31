from flask import Flask, render_template, jsonify, request
from sudoku_generator import SudokuGenerator

app = Flask(__name__)
generator = SudokuGenerator()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/api/check-uniqueness', methods=['POST'])
def check_uniqueness():
    """Check if the given board has exactly one solution. Expects JSON: { board: 9x9 grid }."""
    data = request.get_json()
    if not data or 'board' not in data:
        return jsonify({'error': 'Missing board'}), 400
    board = data['board']
    if not isinstance(board, list) or len(board) != 9 or any(not isinstance(row, list) or len(row) != 9 for row in board):
        return jsonify({'error': 'Invalid board shape'}), 400
    count = generator.count_solutions(board, limit=2)
    return jsonify({'unique': count == 1, 'solutions': count})

@app.route('/api/solve', methods=['POST'])
def solve_board():
    """If the board has exactly one solution, return it. Expects JSON: { board: 9x9 grid }."""
    data = request.get_json()
    if not data or 'board' not in data:
        return jsonify({'error': 'Missing board'}), 400
    board = data['board']
    if not isinstance(board, list) or len(board) != 9 or any(not isinstance(row, list) or len(row) != 9 for row in board):
        return jsonify({'error': 'Invalid board shape'}), 400
    solution = generator.get_solution(board)
    if solution is None:
        return jsonify({'error': 'No unique solution'}), 400
    return jsonify({'solution': solution})

@app.route('/api/generate', methods=['GET'])
def generate_sudoku():
    """API endpoint to generate a new fully filled Sudoku board."""
    board = generator.generate()
    return jsonify({'board': board})

@app.route('/api/generate-puzzle', methods=['GET'])
def generate_puzzle():
    """API endpoint to generate a playable puzzle (one solution, medium difficulty)."""
    puzzle, solution = generator.generate_puzzle(clue_count=34)
    return jsonify({'board': puzzle, 'solution': solution})

@app.route('/api/generate-greater-than', methods=['GET'])
def generate_greater_than():
    """Generate a Greater Than Sudoku uniquely solvable via sudoku rules + inequalities."""
    puzzle, solution, h_signs, v_signs = generator.generate_puzzle_gt(target_clues=20)
    return jsonify({'puzzle': puzzle, 'solution': solution, 'h_signs': h_signs, 'v_signs': v_signs})

@app.route('/api/generate-next-to-nine', methods=['GET'])
def generate_next_to_nine():
    """Generate a Next-to-Nine Sudoku puzzle."""
    puzzle, solution, row_clues, col_clues = generator.generate_puzzle_n2n()
    return jsonify({'puzzle': puzzle, 'solution': solution, 'row_clues': row_clues, 'col_clues': col_clues})

@app.route('/api/generate-thermo', methods=['GET'])
def generate_thermo():
    """Generate a Thermometer Sudoku puzzle."""
    puzzle, solution, thermos = generator.generate_puzzle_thermo(n_thermos=7, target_clues=20)
    return jsonify({'puzzle': puzzle, 'solution': solution, 'thermos': thermos})

@app.route('/api/generate-corner', methods=['GET'])
def generate_corner():
    """Generate a Quad Clues Sudoku puzzle."""
    puzzle, solution, corner_clues = generator.generate_puzzle_corner(n_corners=20, target_clues=8)
    return jsonify({'puzzle': puzzle, 'solution': solution, 'corner_clues': corner_clues})

@app.route('/api/generate-consecutive', methods=['GET'])
def generate_consecutive():
    """Generate a Consecutive Sudoku puzzle uniquely solvable via sudoku rules + consecutive markers."""
    puzzle, solution, h_consec, v_consec = generator.generate_puzzle_consec(target_clues=20)
    return jsonify({'puzzle': puzzle, 'solution': solution, 'h_consec': h_consec, 'v_consec': v_consec})

@app.route('/api/generate/<int:count>', methods=['GET'])
def generate_multiple(count):
    """API endpoint to generate multiple Sudoku boards."""
    if count < 1 or count > 10:
        return jsonify({'error': 'Count must be between 1 and 10'}), 400
    boards = generator.generate_multiple(count)
    return jsonify({'boards': boards})

if __name__ == '__main__':
    app.run(debug=True, port=5001)




