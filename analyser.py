from chomp import Board
from copy import copy


class Analyser:

    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        # all rectangular grids other than 1x1 are definitely winning states (see move stealing argument)
        self.winning_states = {Board(x, y, full_x_size=x_size, full_y_size=y_size)
                               for x in range(1, x_size+1) for y in range(1, y_size+1)}
        self.winning_states.difference_update({Board(1, 1, full_x_size=x_size, full_y_size=y_size)})
        self.losing_states = {Board(1, 1, full_x_size=x_size, full_y_size=y_size)}
        self.to_check_neighbours = {Board(1, 1, full_x_size=x_size, full_y_size=y_size)}
        self.neighbours_checked = set()

    def get_all_previous_states(self, board):
        # TODO
        return set()

    def get_all_next_states(self, board):
        next_states = set()
        for move in (board-{(0, 0)}):
            b = copy(board)
            b.play(move)
            next_states.add(b)
        return next_states

    def analyse_game(self):
        while True:
            try:
                state_to_analyse = self.to_check_neighbours.pop()
                self.analyse_neighbours(state_to_analyse)
            except KeyError:
                return self.losing_states

    def analyse_neighbours(self, state_to_analyse):
        neighbours = self.get_all_previous_states(state_to_analyse)
        for state in neighbours:
            if state not in self.neighbours_checked:
                self.to_check_neighbours.add(state)

            if state not in self.winning_states and state not in self.losing_states:
                # if we haven't calculated whether this state is a winning or losing state yet, do so now
                self.evaluate(state)

        self.neighbours_checked.add(state_to_analyse)

    def evaluate(self, state):
        # Returns True if this state is a winning state, or False if not
        is_winner = self.quick_eval(state)
        if is_winner is not None:
            return is_winner

        for next_state in self.get_all_next_states(state):
            self.evaluate(next_state)
            is_winner = self.quick_eval(state)
            if is_winner is not None:
                return is_winner

        raise Exception("State evaluation failed despite all next states being evaluated")

    def quick_eval(self, state):
        # Returns True if this state is a winning state, False if not, None if unknown yet
        # Also updates self.winning_states/self.losing_states appropriately

        # if any next state is a losing state, this is a winning state
        for next_state in self.get_all_next_states(state):
            if next_state in self.losing_states:
                self.winning_states.add(state)
                return True
        # if every next state is a winning state, this is a losing state
        if self.get_all_next_states(state).issubset(self.winning_states):
            self.losing_states.add(state)
            return False
        return None
