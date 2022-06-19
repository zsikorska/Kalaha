from flask import Flask, render_template, request, redirect, url_for

from aiPlayer import AIPlayer
from board import Board

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('start.html')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.route('/create_account')
def create_account():
    return render_template('create_account.html')


board = Board()
first_player = True
ai = AIPlayer(False)


@app.route('/game', methods=["GET", "POST"])
def player1_move():
    global first_player
    if request.method == 'POST':
        house = int(request.form['house'])
        print(house)
        code = board.move(house, first_player)
        board.print_board()

        if board.is_end_of_game(first_player):
            return redirect('/')

        match code:
            case 0:
                first_player = not first_player
                return redirect('/game')
            case 1:
                print("You have an additional move")
                return redirect('/game')
            case 2:
                print("Wrong number of house")
                return redirect('/')
    else:
        return render_template('board.html', moves=board.possible_moves(first_player), board=board.board)


@app.route('/gameAI', methods=["GET", "POST"])
def user_move():
    if request.method == 'POST':
        house = int(request.form['house'])
        print(house)
        code = board.move(house, True)
        board.print_board()

        if board.is_end_of_game(True):
            return redirect('/')

        match code:
            case 0:
                return ai_move()
            case 1:
                print("You have an additional move")
                return redirect('/gameAI')
            case 2:
                print("Wrong number of house")
                return redirect('/')
    else:
        return render_template('board.html', moves=board.possible_moves(True), board=board.board)


def ai_move():
    house = ai.make_move(board)
    code = board.move(house, False)
    board.print_board()

    if board.is_end_of_game(False):
        return redirect('/')

    match code:
        case 0:
            return redirect('/gameAI')
        case 1:
            print("You have an additional move")
            return ai_move()
        case 2:
            print("Wrong number of house")
            return redirect('/')


if __name__ == '__main__':
    app.run()
