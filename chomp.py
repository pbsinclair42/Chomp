from copy import copy


class Chomp:

    def __init__(self, x_size, y_size):
        self.board = Board(x_size, y_size)
        self.current_player = Player(1)
        self.winner = None
        self.history = []

    def play_move(self, move_reference):
        move_reference = move_reference.upper()
        if move_reference == 'UNDO':
            try:
                old_state = self.history.pop()
                self.board = old_state['board']
                self.current_player = old_state['player']
                return 'Last move undone'
            except IndexError:
                return 'No more moves to undo'
        try:
            move = self.get_coordinates(move_reference)
        except (TypeError, ValueError):
            return "I don't understand {}.".format(move_reference)

        if not self.is_valid(move):
            return '{} seems to be an invalid move.'.format(move_reference)

        self.history.append(self.get_game_state())
        self.board.play(move)
        self.current_player.flip()

        if move_reference == 'A1':
            self.winner = self.current_player()

        return 'Playing move {}'.format(move_reference)

    def is_valid(self, move):
        return move in self.board

    def get_coordinates(self, move_reference):
        x = ord(move_reference[0].upper()) - ord('A')
        y = int(move_reference[1:]) - 1
        return x, y

    def get_game_state(self):
        return {'board': copy(self.board), 'player': copy(self.current_player)}

    def __str__(self):
        return '\n'+str(self.board) + '\n\n'+self.current_player() + " to play."

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.board == other.board and self.current_player == other.current_player

    def __ne__(self, other):
        return not self.__eq__(other)


class Board(set):
    def __init__(self, x_size, y_size, full_x_size=None, full_y_size=None):
        if full_y_size is None:
            full_y_size = y_size
        if full_x_size is None:
            full_x_size = x_size

        if x_size <= 0 or y_size <= 0:
            raise ValueError("Board dimensions must be positive")
        if full_x_size < x_size or full_y_size < y_size:
            raise ValueError("Current size of board must be at most the full size of the board")
        self.x_size = full_x_size
        self.y_size = full_y_size
        set.__init__(self, {(x, y) for x in range(x_size) for y in range(y_size)})

    @classmethod
    def load_from_set(cls, x_size, y_size, board):
        # Warning: does not validate board
        new_board = cls(x_size, y_size)
        super(cls, new_board).__init__(board)
        return new_board

    def play(self, move):
        move_x, move_y = move
        for removed in [(x, y) for x in range(move_x, self.x_size) for y in range(move_y, self.y_size)]:
            try:
                self.remove(removed)
            except KeyError:
                pass

    def flipped(self):
        return self.load_from_set(self.y_size, self.x_size, {(y, x) for (x, y) in self})

    def get_max_x(self, column):
        if column < 0:
            return self.x_size - 1
        if column >= self.y_size:
            return -1
        try:
            return max([x for (x, y) in self if y == column])
        # if column is empty
        except ValueError:
            return -1

    def get_max_y(self, row):
        if row < 0:
            return self.y_size - 1
        if row >= self.x_size:
            return -1
        try:
            return max([y for (x, y) in self if x == row])
        # if row is empty
        except ValueError:
            return -1

    def __str__(self):
        return '\n'.join(' '.join(
            ["*" if (x, y) in self else " " for x in range(self.x_size)]
        ) for y in range(self.y_size - 1, -1, -1))

    def __repr__(self):
        return '\n'+self.__str__()+'\n'

    def __eq__(self, other):
        return str(self) == str(other) or str(self.flipped()) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # boards will have equal hashes iff they are in the same state, including rotations
        return hash(str(self)) + hash(str(self.flipped()))

    def __copy__(self):
        return self.load_from_set(self.x_size, self.y_size, self)


class Player:
    def __init__(self, n):
        self.n = n

    def flip(self):
        if self.n == 1:
            self.n = 2
        else:
            self.n = 1

    def __str__(self):
        return "Player " + str(self.n)

    def __repr__(self):
        return str(self)

    def __call__(self):
        return str(self)

    def __eq__(self, other):
        return self.n == other

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == '__main__':
    while True:
        try:
            x_size, y_size = input("Enter grid size: ").split(',')
            x_size, y_size = int(x_size), int(y_size)
            break
        except Exception as e:
            pass
    chomp = Chomp(x_size, y_size)
    while True:
        try:
            print(chomp)
            this_move = str(input("Enter move: "))
            print(chomp.play_move(this_move))
            if chomp.winner is not None:
                print()
                print(chomp.current_player() + " wins!")
                break
        except Exception as e:
            print(e.__class__)
            print(e)
            pass
