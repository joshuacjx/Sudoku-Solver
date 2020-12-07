# Sudoku Solver
This is a simple Python script that is able to solve any partially-filled Sudoku input instantly.

## Usage Instructions
Go to the 'Releases' section and download the .zip file corresponding to your OS. Unzip the file and double-click on the executable `Sudoku Solver V1` to run it.
For MacOS users, your computer might not allow you to run the executable due to security reasons. If this happens, go to `System Preferences > Security & Privacy > Open Anyway` to allow your computer to open the app.

Alternatively, clone this repository in your Desktop. Next, run `python gui.py` in your Command Line.

## GUI
The Graphic User Interface (GUI) is made using the Python Tkinter library. Its source code is found in the module `gui.py`.

Some suggestions for future extensions include:
- Changing the colour for the input fields to black once the input has been changed.
- Allowing the GUI to output all pairs of conflicting assignments instead of just one.
- Colour-coding the different subgrids to make the GUI more visually intuituve.
- Allow Sudoku interface to remain in the middle of the window when the window is resized.

## Backend
The Sudoku is solved using the Backtrack Search algorithm learnt in an Artifical Intelligence module in NUS. Its source code is found in the module `sudoku.py`.

Some suggestions for future extensions include:
- Making the script more Pythonic
- Refactor the backend code such that the classes follow Software Engineering principles.
- Make the GUI follow the Observer design pattern such that it is updated every time an assignment is made or removed, so that the user can visualise the backtracking algorithm.
