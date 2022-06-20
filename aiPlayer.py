import random

from player import Player

DEPTH = 4


class AIPlayer(Player):

    def __init__(self, first):
        self.first = first
        self.level = 0

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    def make_move(self, board):
        if random.randint(1, 4) < self.level:
            return self.smart_move(board)
        else:
            return self.random_move(board)

    def smart_move(self, board):
        print('smart')
        list_of_moves = []
        max_diff = float('-inf')
        best_move = -1

        for house in board.possible_moves(self.first):
            new_board = board.clone()
            code = new_board.move(house, self.first)

            if code == 1:  # additional move
                list_of_moves.append((self.min_max_algorithm(new_board, DEPTH, True), house))
            else:
                list_of_moves.append((self.min_max_algorithm(new_board, DEPTH - 1, False), house))

        for (diff, move) in list_of_moves:
            if diff > max_diff or (diff == max_diff and move > best_move):
                max_diff = diff
                best_move = move

        print(best_move)
        return best_move

    '''
    isEndOfGame(first == maximizingPlayer)
    first - true, maximizingPlayer - true => isEndOfGame(true) player1 should move
    first - true, maximizingPlayer - false => isEndOfGame(false) player2 should move
    first - false, maximizingPlayer - true => isEndOfGame(false) player2 should move
    first - false, maximizingPlayer - false => isEndOfGame(true) player1 should move
    '''

    def min_max_algorithm(self, board, depth, maximizing_player):
        if depth == 0:
            return board.count_difference(self.first)

        elif board.is_end_of_game(self.first == maximizing_player):
            board.end_of_game(self.first == maximizing_player)
            return board.count_difference(self.first)

        elif maximizing_player:
            max_diff = float('-inf')

            for house in board.possible_moves(self.first):
                new_board = board.clone()
                code = new_board.move(house, self.first)

                if code == 1:
                    diff = self.min_max_algorithm(new_board, depth, True)
                else:
                    diff = self.min_max_algorithm(new_board, depth - 1, False)

                if diff > max_diff:
                    max_diff = diff

            return max_diff

        else:
            min_diff = float('inf')

            for house in board.possible_moves(not self.first):
                new_board = board.clone()
                code = new_board.move(house, not self.first)

                if code == 1:
                    diff = self.min_max_algorithm(new_board, depth, False)
                else:
                    diff = self.min_max_algorithm(new_board, depth - 1, True)

                if diff < min_diff:
                    min_diff = diff

            return min_diff

    def random_move(self, board):
        print('random')
        house = -1

        while not board.check_house(house, self.first):
            if self.first:
                house = random.randint(0, 5)
            else:
                house = random.randint(7, 12)

        print(house)
        return house
