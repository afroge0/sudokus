# Sudoku Generator

A web application that generates fully filled 9x9 Sudoku boards that satisfy all Sudoku rules.

## Features

- Generates valid, fully filled 9x9 Sudoku boards
- Beautiful, user-friendly web interface
- Fast generation using backtracking algorithm
- Responsive design that works on desktop and mobile

## Setup

1. Install Python 3.7 or higher

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## How It Works

The Sudoku generator uses a backtracking algorithm to fill a 9x9 grid such that:
- Each row contains digits 1-9 exactly once
- Each column contains digits 1-9 exactly once
- Each 3x3 box contains digits 1-9 exactly once

The algorithm randomly shuffles the order of numbers tried at each position, ensuring variety in the generated boards.

## Usage

- Click "Generate New Board" to create a single new Sudoku board
- Click "Generate 5 Boards" to generate multiple boards at once

## Project Structure

```
sudokus/
├── app.py                 # Flask web server
├── sudoku_generator.py    # Sudoku generation logic
├── templates/
│   └── index.html        # Web interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

