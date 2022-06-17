from player import Player


class HumanPlayer(Player):

    def __init__(self, first):
        self.first = first

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value

    def make_move(self, board):
        house = -1

        try:
            house = int(input())
        except ValueError:
            print("This is not a number.")
            if self.first:
                print("Player1's move: ")
            else:
                print("Player2's move: ")
            house = self.make_move(board)

        return house
