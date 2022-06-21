class Board:
    """
    Class represents the board of the game:
    board[0] - board[5] -> player1's houses
    board[6] -> player1's base
    board[7] - board[12] -> player2's houses
    board[13] -> player2's base
    player1 begins the game
    first - True if player1, False if player2
    """

    def __init__(self):
        self.board = [4 for i in range(14)]
        self.board[13] = 0
        self.board[6] = 0

    '''
    Codes returned by def move:
    0 => next player moves
    1 => this player has additional move
    2 => wrong move
    '''

    # Function for moving from specific house by specific player
    def move(self, house, first):
        code = 0

        if not self.check_house(house, first):
            code = 2
        else:
            number_of_stones = self.board[house]
            self.board[house] = 0
            next_house = house

            # Moving stones from house, each stone to the next house (and player's base)
            while number_of_stones > 0:
                next_house = (next_house + 1) % 14
                if (first and next_house == 13) or (not first and next_house == 6):
                    next_house = (next_house + 1) % 14

                self.board[next_house] += 1
                number_of_stones -= 1

            if self.last_stone_in_base(first, next_house):
                code = 1
            else:
                self.take_opposite_stones(first, next_house)

        return code

    # Function returns True if last stone lands in the player's base
    @staticmethod
    def last_stone_in_base(first, last_house):
        if first and last_house == 6:
            return True
        elif not first and last_house == 13:
            return True
        else:
            return False

    # Function takes stones of opponent if last stone lands in empty house and opponent has stones in opposite house
    # True if stones were taken
    def take_opposite_stones(self, first, last_house):
        if self.board[last_house] == 1 and self.board[12 - last_house] != 0:
            if first and last_house <= 5:
                self.board[6] += self.board[12 - last_house] + 1
                self.board[12 - last_house] = 0
                self.board[last_house] = 0
                return True
            elif not first and last_house >= 7:
                self.board[13] += self.board[12 - last_house] + 1
                self.board[12 - last_house] = 0
                self.board[last_house] = 0
                return True
        return False

    # Function checks if player chose the right house
    def check_house(self, house, first):
        if house < 0 or house > 13:
            return False
        elif house == 6 or house == 13:
            return False
        elif self.board[house] == 0:
            return False
        elif first:
            return house <= 5
        else:
            return house >= 7

    # Function returns the list of possible moves (numbers of houses from which player can move)
    def possible_moves(self, first):
        list_of_moves = []
        if first:
            for i in range(6):
                if self.board[i] != 0:
                    list_of_moves.append(i)
        else:
            for i in range(7, 13):
                if self.board[i] != 0:
                    list_of_moves.append(i)
        return list_of_moves

    # Function moves stones of the player's opponent to his base
    # It happens when it's the end of game and player does not have possible moves
    def end_of_game(self, first):
        if first:
            for i in range(7, 13):
                self.board[13] += self.board[i]
                self.board[i] = 0
        else:
            for i in range(6):
                self.board[6] += self.board[i]
                self.board[i] = 0

    # Function checks if player has possible moves
    def is_end_of_game(self, first):
        return self.possible_moves(first) == []

    # Function counts the deficit between bases of the players
    def count_difference(self, first):
        if first:
            return self.board[6] - self.board[13]
        else:
            return self.board[13] - self.board[6]

    # Function returns the cloned board
    def clone(self):
        new_board = Board()
        for i in range(14):
            new_board.board[i] = self.board[i]
        return new_board

    # Function refreshes the board to the start settings
    def refresh(self):
        self.board = [4 for i in range(14)]
        self.board[13] = 0
        self.board[6] = 0
