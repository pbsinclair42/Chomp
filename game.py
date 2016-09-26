from chomp import Chomp
from analyser import Analyser
from datetime import datetime, timedelta
from time import sleep
from random import randint, sample


if __name__ == '__main__':
    while True:
        try:
            x_size, y_size = input("Enter grid size: ").split(',')
            x_size, y_size = int(x_size), int(y_size)
            break
        except Exception as e:
            pass
    chomp = Chomp(x_size, y_size)
    analyser = Analyser(x_size, y_size)
    while True:
        num_players = input("One or two players? ")
        if num_players=="1" or num_players=="2":
            num_players = int(num_players)
            break
        elif num_players.lower() == "one":
            num_players = 1
            break
        elif num_players.lower() == "two":
            num_players = 2
            break

    player = 'human' if num_players==2 or randint(0,1)==0 else 'computer'
    while True:
        print(chomp)
        if player=='human':
            # user move
            this_move = str(input("Enter move: "))
        else:
            # computer move
            time_taken = datetime.now()
            print("Thinking...")
            this_move = analyser.find_winning_move(chomp.board)
            if this_move is None:
                print("Playing randomly!")
                this_move = sample(chomp.board, 1)[0]
            this_move = chr(this_move[0]+ord('A')) + str(this_move[1]+1)
            if datetime.now()-timedelta(seconds=1)<time_taken:
                sleep(1)

        message = chomp.play_move(this_move)
        print(message)
        if chomp.winner is not None:
            print()
            print(chomp.current_player() + " wins!")
            break
        if message[:13]=='Playing move ':
            player = 'human' if num_players == 2 or player == 'computer' else 'computer'
