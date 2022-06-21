import random

DEPTH = 4


class AIPlayer:
    """
    Class represents the AI (computer):
    level - higher - AI makes smarter moves based on decision tree, lower - AI makes more random moves
    first - True if player1, False if player2
    player1 begins the game
    """

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

    # Function returns the number of house from which AI wants to move
    # level 0<= -> AI makes only random moves
    # level >=5 -> AI makes only smart moves
    def make_move(self, board):
        if random.randint(1, 4) < self.level:
            return self.smart_move(board)
        else:
            return self.random_move(board)

    # Function returns the number of house which is the effect of calculation of deficit between bases
    def smart_move(self, board):
        list_of_moves = []
        max_diff = float('-inf')
        best_move = -1

        # For all the possible moves calculate the deficit between bases after DEPTH number of player's changes
        for house in board.possible_moves(self.first):
            new_board = board.clone()   # clone board not to destroy the used one
            code = new_board.move(house, self.first)

            if code == 1:  # additional move
                list_of_moves.append((self.min_max_algorithm(new_board, DEPTH, True), house))
            else:   # change of players
                list_of_moves.append((self.min_max_algorithm(new_board, DEPTH - 1, False), house))

        # Choose the move with the biggest deficit of points
        for (diff, move) in list_of_moves:
            if diff > max_diff or (diff == max_diff and move > best_move):
                max_diff = diff
                best_move = move

        return best_move

    '''
    isEndOfGame(first == maximizingPlayer)
    first - true, maximizingPlayer - true => isEndOfGame(true) - player1's turn
    first - true, maximizingPlayer - false => isEndOfGame(false) - player2's turn
    first - false, maximizingPlayer - true => isEndOfGame(false) - player2's turn
    first - false, maximizingPlayer - false => isEndOfGame(true) - player1's turn
    '''
    # Function return the best deficit between bases after DEPTH number of player's changes
    # Creates decision tree by recursion and returns the best path
    # depth - depth of the recursion tree (number of player's changes)
    # maximizing_player - True if it is an AI turn to move (AI wants to maximize the deficit),
    # False if it is AI's opponents turn (opponent wants to minimize the deficit)
    def min_max_algorithm(self, board, depth, maximizing_player):
        if depth == 0:
            return board.count_difference(self.first)   # count the deficit from AI perspective

        # current player does not have possible moves = end of game
        elif board.is_end_of_game(self.first == maximizing_player):
            board.end_of_game(self.first == maximizing_player)
            return board.count_difference(self.first)   # count the deficit from AI perspective

        # AI's turn
        elif maximizing_player:
            max_diff = float('-inf')

            for house in board.possible_moves(self.first):
                new_board = board.clone()
                code = new_board.move(house, self.first)

                if code == 1:   # additional move
                    diff = self.min_max_algorithm(new_board, depth, True)
                else:   # change of players
                    diff = self.min_max_algorithm(new_board, depth - 1, False)

                if diff > max_diff:
                    max_diff = diff

            return max_diff

        # AI's opponents turn
        else:
            min_diff = float('inf')

            for house in board.possible_moves(not self.first):
                new_board = board.clone()
                code = new_board.move(house, not self.first)

                if code == 1:   # additional move
                    diff = self.min_max_algorithm(new_board, depth, False)
                else:   # change of players
                    diff = self.min_max_algorithm(new_board, depth - 1, True)

                if diff < min_diff:
                    min_diff = diff

            return min_diff

    # Function returns the random number of house (which contains >0 stones)
    def random_move(self, board):
        house = -1

        while not board.check_house(house, self.first):
            if self.first:
                house = random.randint(0, 5)
            else:
                house = random.randint(7, 12)

        return house
