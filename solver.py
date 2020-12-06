class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve(self):
        initial_assignment = self.get_initial_assignment()
        if not initial_assignment.is_valid():
            return "Cannot be solved!"
        completed_assignment = backtrack(initial_assignment, self)
        return Sudoku.to_string(self.get_answer_grid(completed_assignment))

    def get_initial_assignment(self):
        initial_assignment = Assignment()
        for row in range(9):
            for col in range(9):
                val = self.puzzle[row][col]
                if val is not 0:
                    initial_assignment.add_assignment((row, col), val)
        return initial_assignment

    def get_answer_grid(self, completed_assignment):
        answer_grid = [[0 for col in range(9)] for row in range(9)]
        for pos in completed_assignment.pos_to_value:
            answer_grid[pos[0]][pos[1]] = completed_assignment.pos_to_value[pos]
        return answer_grid

    @staticmethod
    def to_string(answer_grid):
        answer = "Solution:" + '\n'
        for row in range(9):
            for col in range(9):
                answer += str(answer_grid[row][col])
            answer += '\n'
        return answer


def backtrack(assignment, sudoku):
    if assignment.is_complete():
        return assignment
    pos = select_unassigned_pos(assignment, sudoku)
    for val in order_domain_value(pos, assignment):
        if assignment.is_consistent_with(pos, val):
            what_changed_from_assignment = assignment.add_assignment(pos, val)
            result = backtrack(assignment, sudoku)
            if result is not None:
                return result
            assignment.remove_assignment(pos, val, what_changed_from_assignment)
    return None


def select_unassigned_pos(assignment, sudoku):
    if assignment.is_empty():
        return (0, 0)
    # Initialize to invalid value first
    most_constrained_pos = (9, 9)
    min_num_remaining_value = 9
    for row in range(9):
        for col in range(9):
            if sudoku.puzzle[row][col] is 0:
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


class Assignment(object):
    def __init__(self):
        self.pos_to_value = dict()
        self.pos_to_domain = dict()
        self.val_to_num_constrained = dict()
        self.constrained = dict()
        self.initialize()

    def initialize(self):
        for row in range(9):
            for col in range(9):
                self.pos_to_domain[(row, col)] = set(range(1, 10))

        for val in range(1, 10):
            self.val_to_num_constrained[val] = 0

        rows = dict()
        for row in range(9):
            rows[row] = {(row, col) for col in range(9)}
        cols = dict()
        for col in range(9):
            cols[col] = {(row, col) for row in range(9)}
        subgrids = dict()
        for subgrid in range(9):
            subgrids[subgrid] = get_positions_at_subgrid(subgrid)
        for row in range(9):
            for col in range(9):
                subgrid = get_subgrid_index(row, col)
                self.constrained[(row, col)] = (rows[row] | cols[col] | subgrids[subgrid])

    def get_domain(self, pos):
        return self.pos_to_domain[pos]

    def is_assigned(self, pos):
        return pos in self.pos_to_value

    def is_complete(self):
        return len(self.pos_to_value) is 81

    def is_empty(self):
        return not self.pos_to_value

    def is_valid(self):
        for pos in self.pos_to_value:
            for other_pos in self.pos_to_value:
                is_different_pos = pos is not other_pos
                is_constrained = other_pos in self.constrained[pos]
                is_same_value = self.pos_to_value[pos] is self.pos_to_value[other_pos]
                if is_different_pos and is_constrained and is_same_value:
                    return False
        return True

    def is_consistent_with(self, pos, val):
        return val in self.pos_to_domain[pos]

    def add_assignment(self, pos, val):
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

    def remove_assignment(self, pos, val, what_needs_to_be_returned):
        self.pos_to_value.pop(pos)
        for other_pos in what_needs_to_be_returned.keys():
            for value_to_return in what_needs_to_be_returned[other_pos]:
                self.pos_to_domain[other_pos].add(value_to_return)
                self.val_to_num_constrained[val] -= 1

    def get_num_pos_constrained_by_val(self, val):
        return self.val_to_num_constrained[val]


def get_subgrid_index(row, col):
    i = int(row / 3)
    j = int(col / 3)
    if i is 0:
        return i + j
    elif i is 1:
        return i + j + 2
    else:
        return i + j + 4


def get_positions_at_subgrid(subgrid):
    top_lefts = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
    top_left = top_lefts[subgrid]
    positions = set()
    for i in range(0, 3):
        for j in range(0, 3):
            positions.add((top_left[0] + i, top_left[1] + j))
    return positions