class Board:
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

    def move(self, house, first):
        code = 0

        if not self.check_house(house, first):
            code = 2
        else:
            number_of_stones = self.board[house]
            self.board[house] = 0
            next_house = house

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

    @staticmethod
    def last_stone_in_base(first, last_house):
        if first and last_house == 6:
            return True
        elif not first and last_house == 13:
            return True
        else:
            return False

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

    def end_of_game(self, first):
        if first:
            for i in range(7, 13):
                self.board[13] += self.board[i]
                self.board[i] = 0
        else:
            for i in range(6):
                self.board[6] += self.board[i]
                self.board[i] = 0

    def is_end_of_game(self, first):
        return self.possible_moves(first) == []

    def print_who_win(self):
        print()
        print("##### Results #####")
        print("\n%8s %3s %8s" % ("player1", "vs", "player2"))
        print("\n%4d %8s %4d \n" % (self.board[6], "", self.board[13]))

        if self.board[6] > self.board[13]:
            print("Player1 won !!!")
        elif self.board[6] == self.board[13]:
            print("Draw !!!")
        else:
            print("Player2 won !!!")

    def count_difference(self, first):
        if first:
            return self.board[6] - self.board[13]
        else:
            return self.board[13] - self.board[6]

    def clone(self):
        new_board = Board()
        for i in range(14):
            new_board.board[i] = self.board[i]
        return new_board

    def print_board(self):
        print()
        print("%20s" % "Player2")
        print("%1s%4s %4s %4s %4s %4s %4s" % (" ", "12", "11", "10", "9", "8", "7"))
        line = " "
        for i in range(32):
            line += "-"
        print(line)
        print("%1s%4d %4d %4d %4d %4d %4d%3s%1s" % ("|", self.board[12], self.board[11], self.board[10],
              self.board[9], self.board[8], self.board[7], " ", "|"))
        print("%1s%4d %19s %4d%3s%1s" % ("|", self.board[13], "", self.board[6], " ", "|"))
        print("%1s%4d %4d %4d %4d %4d %4d%3s%1s" % ("|", self.board[0], self.board[1], self.board[2], self.board[3],
              self.board[4], self.board[5], " ", "|"))
        print(line)
        print("%1s%4s %4s %4s %4s %4s %4s" % (" ", "0", "1", "2", "3", "4", "5"))
        print("%20s \n" % "Player1")

    def refresh(self):
        self.board = [4 for i in range(14)]
        self.board[13] = 0
        self.board[6] = 0
