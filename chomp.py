class Chomp:

    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.board = {(x, y): True for x in range(x_size) for y in range(y_size)}
        self.current_player = Player(1)
        self.winner = None

    def play_move(self, move_reference):
        move_reference = move_reference.upper()
        try:
            move = get_coordinates(move_reference)
        except TypeError:
            return "I don't understand {}.".format(move_reference)

        if not self.is_valid(move):
            return '{} seems to be an invalid move.'.format(move_reference)

        for move in [(x, y) for x in range(move[0], self.x_size) for y in range(move[1], self.y_size)]:
            self.board[move] = False
        self.current_player.flip()

        if move_reference == 'A1':
            self.winner = self.current_player()

        return 'Playing move {}'.format(move_reference)

    def is_valid(self, move):
        return self.board.get(move, False)

    def get_coordinates(move_reference):
        x = ord(move_reference[0].upper()) - ord('A')
        y = int(move_reference[1:]) - 1
        return x, y

    def __str__(self):
        return '\n'.join(' '.join(
                ["*" if self.board[(x, y)] else " " for x in range(self.x_size)]
            ) for y in range(self.y_size - 1, -1, -1))
    
    def __repr__(self):
        return self.__str__()


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
            print(chomp.current_player() + " to play.")
            this_move = str(input("Enter move: "))
            print(chomp.play_move(this_move))
            if chomp.winner is not None:
                print(chomp.current_player() + " wins!")
                break
        except Exception as e:
            pass
