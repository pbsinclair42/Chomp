from chomp import Board


class Analyser:

    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        # all rectangular grids are definitely winning states (see move stealing argument)
        self.winning_states = {Board(x,y) for x in range(1, x_size+1) for y in range(1, y_size+1)}
        self.winning_states.difference_update({Board(1,1)})
        self.losing_states = {Board(1, 1)}
        self.to_check = {Board(1,1): False, **{state:True for state in self.winning_states}}


    def analyse(self):
        try:
            state_to_analyse, is_winning = self.to_check.popitem()
        except KeyError:
            return self.winning_states
