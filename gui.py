from tkinter import *
from solver import Sudoku


class SudokuInterface():
    def __init__(self, frame):
        self.cells = self.get_empty_cells(frame)

    def get_empty_cells(self, frame):
        cells = [[(rw, cl) for cl in range(9)] for rw in range(9)]
        register = frame.register(SudokuInterface.is_valid_cell_input)
        for rw in range(9):
            for cl in range(9):
                # Create a cell for that Sudoku entry
                cell = Entry(frame, width=2, justify=CENTER)
                # Configure the cell to conform to input validation
                cell.config(validate="key", validatecommand=(register, '%P'))
                cells[rw][cl] = cell
                # Display the cell onto the GUI
                cell.grid(row=rw, column=cl)
        return cells

    @staticmethod
    def is_valid_cell_input(input):
        if input is "":
            return True
        if input.isdigit():
            return 1 <= int(input) <= 9
        return False

    def make_sudoku(self):
        puzzle = [[(rw, cl) for cl in range(9)] for rw in range(9)]
        for rw in range(9):
            for cl in range(9):
                input = self.cells[rw][cl].get()
                if input is "":
                    puzzle[rw][cl] = 0
                if input.isdigit():
                    puzzle[rw][cl] = int(input)
        return Sudoku(puzzle)


root = Tk()
root.title("Sudoku Solver")

instruction = Label(root, text="Input your Sudoku puzzle below!")
instruction.grid(row=0)

sudokuFrame = Frame(root)
sudokuFrame.grid(row=1)

entries = SudokuInterface(sudokuFrame)


def get_solution():
    sudoku = entries.make_sudoku()
    answer = sudoku.solve()
    Label(root, text=answer, font="Arial").grid()


solveButton = Button(root, text="Solve", command=get_solution)
solveButton.grid()


root.mainloop()
