# Sudokus Project

A Flask web app that generates and serves various Sudoku puzzle variants.

## Stack

- **Backend**: Python / Flask (`app.py`)
- **Puzzle logic**: `sudoku_generator.py` — `SudokuGenerator` class with backtracking solver
- **Frontend**: Vanilla JS (`SudokuBoard` class), HTML/CSS in `templates/index.html`
- **Python**: 3.14, virtual environment in `venv/`

## Running the app

```bash
source venv/bin/activate
python app.py
# Runs on http://localhost:5001
```

## Project structure

```
app.py                  # Flask routes / API endpoints
sudoku_generator.py     # Puzzle generation logic
templates/index.html    # Single-page frontend
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/generate` | Fully filled board |
| GET | `/api/generate-puzzle` | Standard puzzle (34 clues) |
| GET | `/api/generate-greater-than` | Greater-Than variant |
| GET | `/api/generate-next-to-nine` | Next-to-Nine variant |
| GET | `/api/generate-thermo` | Thermometer variant |
| GET | `/api/generate-corner` | Quad Clues variant |
| GET | `/api/generate-consecutive` | Consecutive variant |
| GET | `/api/generate/<count>` | Multiple boards (1–10) |
| POST | `/api/check-uniqueness` | Check if board has one solution |
| POST | `/api/solve` | Return the unique solution |

## Puzzle variants

- **Greater Than**: cells constrained by `<`/`>` inequality signs between neighbours
- **Next-to-Nine**: clues indicate which rows/cols contain a 9 adjacent to a given cell
- **Thermometer**: digits must increase along thermometer paths
- **Quad Clues (Corner)**: corner markers show which digits appear in the surrounding 4 cells
- **Consecutive**: markers between adjacent cells that differ by exactly 1
