from enum import Enum


class SudokuState(Enum):
    NOT_SOLVED_YET = 0
    SOLVED = 1
    UNSOLVABLE = 2


class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.state = SudokuState.NOT_SOLVED_YET
        self.invalid_data = dict()

    def solve(self):
        initial_assignment = self.get_initial_assignment()
        if not initial_assignment.is_valid():
            self.state = SudokuState.UNSOLVABLE
            self.invalid_data = initial_assignment.get_invalid_assignment()
            return self.get_invalid_assignment_message()
        completed_assignment = backtrack(initial_assignment, self)
        self.state = SudokuState.SOLVED
        return Sudoku.get_answer_string(self.get_answer_grid(completed_assignment))

    def get_invalid_assignment(self):
        if not self.invalid_data:
            return None
        return self.invalid_data

    def get_invalid_assignment_message(self):
        if not self.invalid_data:
            return None
        positions = self.invalid_data["conflicting-positions"]
        value = self.invalid_data["value-assigned"]
        errorString = "Cannot be solved!" + '\n' \
                      + str(positions[0]) + " and " + str(positions[1]) \
                      + " cannot both be " + str(value) + "."
        return errorString

    def get_state(self):
        return self.state

    def get_initial_assignment(self):
        initial_assignment = Assignment()
        for row in range(9):
            for col in range(9):
                val = self.grid[row][col]
                if val is not 0:
                    initial_assignment.add((row, col), val)
        return initial_assignment

    def get_answer_grid(self, completed_assignment):
        answer_grid = [[0 for col in range(9)] for row in range(9)]
        for pos in completed_assignment.pos_to_value:
            answer_grid[pos[0]][pos[1]] = completed_assignment.pos_to_value[pos]
        return answer_grid

    @staticmethod
    def get_answer_string(answer_grid):
        answer = "Solution:" + '\n'
        for row in range(9):
            for col in range(9):
                answer += str(answer_grid[row][col]) + "  "
            answer += '\n'
        return answer

    @staticmethod
    def get_subgrid_index(row, col):
        i = int(row / 3)
        j = int(col / 3)
        if i is 0:
            return i + j
        elif i is 1:
            return i + j + 2
        else:
            return i + j + 4

    @staticmethod
    def get_positions_at_subgrid(subgrid):
        top_lefts = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        top_left = top_lefts[subgrid]
        positions = set()
        for i in range(0, 3):
            for j in range(0, 3):
                positions.add((top_left[0] + i, top_left[1] + j))
        return positions


class Assignment:
    """Encapsulates the state of assignment of values to positions in a Sudoku grid."""

    NUM_POSITIONS = 81
    ALL_POSITIONS = sum([[(row, col) for col in range(9)] for row in range(9)], [])

    def __init__(self):
        self.pos_to_value = dict()
        """Maps every position (row, col) to a value within the range [0, 9]."""

        self.pos_to_domain = dict()
        """Maps position (row, col) to the set of values it can possibly 
        take given the current state of assignment."""
        [self.pos_to_domain.setdefault(pos, set(range(1, 10))) for pos in Assignment.ALL_POSITIONS]

        self.val_to_num_constrained = dict().fromkeys(range(1, 10), 0)
        """Maps values (within the range [0, 9]) to the number of positions 
        unable to be assigned to that value."""

        self.constrained = dict()
        """Maps position (row, col) to a set of positions constrained by the 
        position (i.e. same row, column or subgrid)."""

        rows_to_positions = {row: set((row, col) for col in range(9)) for row in range(9)}
        cols_to_positions = {col: set((row, col) for row in range(9)) for col in range(9)}
        subgrids_to_positions = {subgrid: Sudoku.get_positions_at_subgrid(subgrid) for subgrid in range(9)}

        self.constrained = {(row, col): (rows_to_positions[row]
                                         | cols_to_positions[col]
                                         | subgrids_to_positions[Sudoku.get_subgrid_index(row, col)])
            for (row, col) in Assignment.ALL_POSITIONS}


    def get_domain(self, pos):
        return self.pos_to_domain[pos]

    def is_assigned(self, pos):
        return pos in self.pos_to_value

    def is_complete(self):
        return len(self.pos_to_value) is Assignment.NUM_POSITIONS

    def is_empty(self):
        return not self.pos_to_value

    def is_conflicting(self, pos, other_pos):
        is_different_pos = pos is not other_pos
        is_constrained = other_pos in self.constrained[pos]
        is_same_value = self.pos_to_value[pos] is self.pos_to_value[other_pos]
        return is_different_pos and is_constrained and is_same_value

    def is_valid(self):
        for pos in self.pos_to_value:
            for other_pos in self.pos_to_value:
                if self.is_conflicting(pos, other_pos):
                    return False
        return True

    def get_invalid_assignment(self):
        if self.is_valid():
            return None
        for pos in self.pos_to_value:
            for other_pos in self.pos_to_value:
                if self.is_conflicting(pos, other_pos):
                    error_data = dict()
                    error_data["value-assigned"] = self.pos_to_value[pos]
                    error_data["conflicting-positions"] = [pos, other_pos]
                    return error_data

    def is_consistent_with(self, pos, val):
        return val in self.pos_to_domain[pos]

    def add(self, pos, val):
        self.pos_to_value[pos] = val
        what_was_removed = dict()
        for other_pos in self.constrained[pos]:
            if val in self.get_domain(other_pos):
                self.pos_to_domain[other_pos].discard(val)
                self.val_to_num_constrained[val] += 1
                if other_pos not in what_was_removed:
                    what_was_removed[other_pos] = set()
                what_was_removed[other_pos].add(val)
        return what_was_removed

    def remove(self, pos, val, what_needs_to_be_returned):
        self.pos_to_value.pop(pos)
        for other_pos in what_needs_to_be_returned.keys():
            for value_to_return in what_needs_to_be_returned[other_pos]:
                self.pos_to_domain[other_pos].add(value_to_return)
                self.val_to_num_constrained[val] -= 1

    def get_num_pos_constrained_by_val(self, val):
        return self.val_to_num_constrained[val]


def backtrack(assignment, sudoku):
    if assignment.is_complete():
        return assignment
    pos = select_unassigned_pos(assignment, sudoku)
    for val in order_domain_value(pos, assignment):
        if assignment.is_consistent_with(pos, val):
            what_changed_from_assignment = assignment.add(pos, val)
            result = backtrack(assignment, sudoku)
            if result is not None:
                return result
            assignment.remove(pos, val, what_changed_from_assignment)
    return None


def select_unassigned_pos(assignment, sudoku):
    if assignment.is_empty():
        return (0, 0)
    # Initialize to invalid value first
    most_constrained_pos = (9, 9)
    min_num_remaining_value = 9
    for row in range(9):
        for col in range(9):
            if sudoku.grid[row][col] is 0:
                if not assignment.is_assigned((row, col)):
                    num_remaining_value = len(assignment.get_domain((row, col)))
                    if num_remaining_value < min_num_remaining_value:
                        min_num_remaining_value = num_remaining_value
                        most_constrained_pos = (row, col)
    return most_constrained_pos


def order_domain_value(pos, assignment):
    val_to_num_constrained_pos = {}
    domain = assignment.get_domain(pos)
    for val in domain:
        num_pos_constrained = assignment.get_num_pos_constrained_by_val(val)
        val_to_num_constrained_pos[val] = num_pos_constrained
    order_domain = [pair[0] for pair in sorted(val_to_num_constrained_pos.items(),
                                                        key=lambda item: item[1])]
    order_domain.reverse()
    return order_domain
