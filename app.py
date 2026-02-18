from flask import Flask, render_template, jsonify
from sudoku_generator import SudokuGenerator

app = Flask(__name__)
generator = SudokuGenerator()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/api/generate', methods=['GET'])
def generate_sudoku():
    """API endpoint to generate a new Sudoku board."""
    board = generator.generate()
    return jsonify({'board': board})

@app.route('/api/generate/<int:count>', methods=['GET'])
def generate_multiple(count):
    """API endpoint to generate multiple Sudoku boards."""
    if count < 1 or count > 10:
        return jsonify({'error': 'Count must be between 1 and 10'}), 400
    boards = generator.generate_multiple(count)
    return jsonify({'boards': boards})

if __name__ == '__main__':
    app.run(debug=True, port=5000)




