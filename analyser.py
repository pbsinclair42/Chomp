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
        last_moves = set()
        for y in range(self.y_size):
            x = board.get_max_x(y)+1
            if x < self.x_size:
                # (x,y) are all the squares adjacent to the remaining squares
                # check that (x-1,y) and (x,y-1) are both in the board or out of bounds
                if (x-1 < 0 or (x-1, y) in board) and (y-1 < 0 or (x, y-1) in board):
                    last_moves.add((x, y))

        last_states = set()

        for (x, y) in last_moves:
            # calculate what this move could have removed
            max_x = board.get_max_x(y-1)
            max_y = board.get_max_y(x-1)
            # so move could have removed stuff from (x, y) to (max_x, max_y)
            x_size = max_x - x + 1
            y_size = max_y - y + 1
            # so size of rectangle of removable stuff is x_size by y_size
            # calculate all possible arrangements of removable points in a rectangle of that size
            arrangements = self.get_possible_numbers_removed_per_column(x_size, y_size)
            # for each arrangement, add those points back in to the board, then save that as a possible previous state
            for arrangement in arrangements:
                b = copy(board)
                for row in range(len(arrangement)):
                    for column in range(arrangement[row]):
                        b.add((x+row, y+column))
                last_states.add(b)

        return last_states

    def get_possible_numbers_removed_per_column(self, x, y):
        # Returns all possible arrangements of squares removed within an x by y grid
        # Sorry for the ugly.  My recursion skills are rusty.
        def loop_rec(n, previous_y, result, xns=None):
            if xns is None:
                xns = []

            if n >= 1:
                for xn in range(previous_y, -1, -1):
                    new_xns = copy(xns)
                    new_xns.append(xn)
                    loop_rec(n-1, xn, result, xns=new_xns)
            else:
                result.append(xns)
        to_return = []
        loop_rec(x, y, to_return)
        # remove the option where no squares are taken
        to_return.pop()
        return to_return

    def get_all_next_states(self, board, with_move=False):
        next_states = set()
        for move in (board-{(0, 0)}):
            b = copy(board)
            b.play(move)
            if with_move:
                next_states.add((b,move))
            else:
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

    def find_winning_move(self, board):
        # if we already know this is a losing state, give up now
        if board in self.losing_states:
            return None
        # try and find a winning move we can make
        possible_moves = self.get_all_next_states(board, with_move=True)
        if len(possible_moves) == 0:
            return None

        # check if we already know if any possible move would be a winning one
        for (state, move) in possible_moves:
            if state in self.losing_states:
                return move
        # keep searching until we find a winning move
        for (state, move) in possible_moves:
            if not self.evaluate(state):
                return move
        # if we've still found nothing, this must be a losing state
        return None
