# Sudoku Generator & Solver

A versatile Sudoku puzzle generator and solver written in Python. 
This program can create and solve Sudoku puzzles of various sizes (e.g., 4x4, 9x9, 16x16) 
and allows users to play interactively through a command-line interface.

## Features

- Generic Board Support: Works with any board size that is a perfect square.

- Unique Puzzle Generation: Creates puzzles that are guaranteed to have only one solution.

- Variable Difficulty: Allows users to choose a difficulty level, which determines the number of visible cells.

- Interactive Gameplay: A command-line interface for players to input their guesses.

- Solver Mode: Can solve any valid Sudoku puzzle

## How to Run

0.Ensure you have Python 3 installed.

1. Clone this repository to your local machine.

2. Maps to the project directory in your terminal.

3. Run the script using the command: python solver.py

## Known Limitations
The backtracking algorithm for ensuring a unique solution is computationally intensive. 
Generating large puzzles (16x16 and above) can be time-consuming

## Future Improvements
1. Improving program performance.

2. Implement a Graphical User Interface (GUI) using Pygame or Tkinter.

3. Develop a more advanced difficulty rating model.

4. Add a "hint" feature for player