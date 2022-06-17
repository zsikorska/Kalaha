from aiPlayer import AIPlayer
from server import Server
from randomPlayer import RandomPlayer
from humanPlayer import HumanPlayer


def print_menu():
    print()
    print("##### Kalaha Game #####")
    print("Choose playing mode: ")
    print("1 <= RandomPlayer vs RandomPlayer")
    print("2 <= RandomPlayer vs HumanPlayer")
    print("3 <= RandomPlayer vs AIPlayer")
    print("4 <= HumanPlayer vs HumanPlayer")
    print("5 <= HumanPlayer vs RandomPlayer")
    print("6 <= HumanPlayer vs AIPlayer")
    print("7 <= AIPlayer vs AIPlayer")
    print("8 <= AIPlayer vs RandomPlayer")
    print("9 <= AIPlayer vs HumanPlayer")
    print()


def choose_mode():
    mode = -1
    try:
        mode = int(input())
    except ValueError:
        print("This is not a number")

    match mode:
        case 1:
            return Server(RandomPlayer(True), RandomPlayer(False))
        case 2:
            return Server(RandomPlayer(True), HumanPlayer(False))
        case 3:
            return Server(RandomPlayer(True), AIPlayer(False))
        case 4:
            return Server(HumanPlayer(True), HumanPlayer(False))
        case 5:
            return Server(HumanPlayer(True), RandomPlayer(False))
        case 6:
            return Server(HumanPlayer(True), AIPlayer(False))
        case 7:
            return Server(AIPlayer(True), AIPlayer(False))
        case 8:
            return Server(AIPlayer(True), RandomPlayer(False))
        case 9:
            return Server(AIPlayer(True), HumanPlayer(False))
        case _:
            print("Choose number between 1 and 9")
            choose_mode()


if __name__ == '__main__':
    print_menu()
    server = choose_mode()
    server.play()
