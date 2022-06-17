from player import Player
import random


class RandomPlayer(Player):

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

        while not board.check_house(house, self.first):
            if self.first:
                house = random.randint(0, 5)
            else:
                house = random.randint(7, 12)

        print(house)
        return house
