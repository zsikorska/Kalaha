from board import Board


class Server:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.current_player = player1

    def change_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play(self):
        self.board.print_board()
        code = 3

        while not self.board.is_end_of_game(self.current_player.first):
            '''
            Codes returned by def move:
            0 => next player moves
            1 => this player has additional move
            2 => wrong move
            '''

            match code:
                case 1:
                    print("You have an additional move")
                case 2:
                    print("Wrong number of house")

            if self.current_player.first:
                print("Player1's move: ")
            else:
                print("Player2's move: ")

            house = self.current_player.make_move(self.board)
            code = self.board.move(house, self.current_player.first)
            if code == 0:
                self.change_player()
            self.board.print_board()

        self.board.end_of_game(self.current_player.first)
        self.board.print_who_win()


