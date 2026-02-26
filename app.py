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

@app.route('/api/generate/<int:count>', methods=['GET'])
def generate_multiple(count):
    """API endpoint to generate multiple Sudoku boards."""
    if count < 1 or count > 10:
        return jsonify({'error': 'Count must be between 1 and 10'}), 400
    boards = generator.generate_multiple(count)
    return jsonify({'boards': boards})

if __name__ == '__main__':
    app.run(debug=True, port=5001)




