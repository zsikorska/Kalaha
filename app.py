from flask import Flask, render_template, request, redirect, flash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models import User, db
from aiPlayer import AIPlayer
from board import Board

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # connect app to database
app.config['SECRET_KEY'] = 'MrSTwDghVkS2zPvhL6rk9oda5tx2ExVKqLoBHZaZvM'  # used to security session cookie
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# create the initial database
@app.before_first_request
def create_all():
    db.create_all()


# reload the user object from the user ID stored in the session
# function should take the str ID of a user, and return the corresponding user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def start():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('start.html')


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        nick = request.form['nick']
        password = request.form['password']

        user = User.query.filter_by(nick=nick).first()  # retrieve a user by nick

        if user is None:
            flash(f"User with the nick {nick} does not exist.")
            return redirect('/sign_in')

        elif bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/home')

        else:
            flash(f"Wrong password for the user {nick}. Try again.")
            return redirect('/sign_in')

    else:
        if current_user.is_authenticated:
            return redirect('/home')
        else:
            return render_template('sign_in.html')


@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    if request.method == 'POST':
        nick = request.form['nick']
        password = request.form['password']
        repeat_password = request.form['repeat password']

        user = User.query.filter_by(nick=nick).first()  # retrieve a user by nick

        if user is not None:
            flash(f"User with the nick {nick} already exists.")
            return redirect('/create_account')

        elif password != repeat_password:
            flash(f"Passwords are not the same.")
            return redirect('/create_account')

        elif len(password) < 6:
            flash(f"Password is too short. It has to be longer than 5 signs.")
            return redirect('/create_account')

        else:
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(nick=nick, password=hashed_password, wins=0, draws=0, loses=0)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/sign_in')
    else:
        if current_user.is_authenticated:
            return redirect('/home')
        else:
            return render_template('create_account.html')


@app.route('/sign_out')
@login_required
def sign_out():
    global running_game

    board.refresh()
    running_game = False
    logout_user()
    return redirect('/')


board = Board()
first_player = True
ai = AIPlayer(False)
mode = 'human'
running_game = False
user_starts = True


@app.route('/game', methods=["GET", "POST"])
@login_required
def play_with_human():
    global first_player
    global mode
    global running_game

    if request.method == 'POST':
        house = int(request.form['house'])
        print(house)
        code = board.move(house, first_player)
        board.print_board()

        match code:
            case 0:
                first_player = not first_player
                return redirect('/game')
            case 1:
                print("You have an additional move")
                return redirect('/game')
    else:
        mode = 'human'
        if board.is_end_of_game(first_player):
            board.end_of_game(first_player)
            update_statistics()
            running_game = False
            return redirect('/results')
        return render_template('board.html', moves=board.possible_moves(first_player), board=board.board)


@app.route('/gameAI', methods=["GET", "POST"])
@login_required
def play_with_ai():
    global mode
    global running_game

    if request.method == 'POST':
        house = int(request.form['house'])
        print(house)
        code = board.move(house, user_starts)
        board.print_board()

        match code:
            case 0:
                return ai_move()
            case 1:
                print("You have an additional move")
                return redirect('/gameAI')
    else:
        mode = 'ai'
        if board.is_end_of_game(user_starts):
            board.end_of_game(user_starts)
            update_statistics()
            running_game = False
            return redirect('/results')
        return render_template('board.html', moves=board.possible_moves(user_starts), board=board.board)


def ai_move():
    global running_game

    if board.is_end_of_game(ai.first):
        board.end_of_game(ai.first)
        update_statistics()
        running_game = False
        return redirect('/results')

    house = ai.make_move(board)
    code = board.move(house, ai.first)
    board.print_board()

    match code:
        case 0:
            return redirect('/gameAI')
        case 1:
            print("You have an additional move")
            return ai_move()


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    global first_player
    global running_game
    global user_starts

    if request.method == 'POST':
        if request.form['play'] == 'human':
            board.refresh()
            running_game = True
            first_player = True
            user_starts = (int(request.form['player']) == 1)
            print(user_starts)
            return redirect('/game')

        elif request.form['play'] == 'ai':
            board.refresh()
            running_game = True
            first_player = True
            user_starts = (int(request.form['player']) == 1)
            print(user_starts)
            ai.first = not user_starts
            ai.level = int(request.form['ai level'])

            if user_starts:
                return redirect('/gameAI')
            else:
                return ai_move()

        elif mode == 'human':
            return redirect('/game')

        else:
            return redirect('/gameAI')

    else:
        print(current_user.nick, current_user.wins, current_user.draws, current_user.loses)
        return render_template('home.html', resume=running_game)


@app.route('/results', methods=["GET", "POST"])
@login_required
def results():
    global first_player
    global running_game

    if request.method == 'POST':
        if request.form['button'] == 'play':
            board.refresh()
            running_game = True
            if mode == 'human':
                first_player = True
                return redirect('/game')
            else:
                if user_starts:
                    return redirect('/gameAI')
                else:
                    return ai_move()
        else:
            return redirect('/home')
    else:
        return render_template('results.html', score1=board.board[6], score2=board.board[13])


def update_statistics():
    if board.board[6] > board.board[13]:
        if user_starts:
            current_user.wins += 1
        else:
            current_user.loses += 1

    elif board.board[6] == board.board[13]:
        current_user.draws += 1

    else:
        if user_starts:
            current_user.loses += 1
        else:
            current_user.wins += 1
    db.session.commit()


@app.route('/statistics', methods=["GET", "POST"])
@login_required
def statistics():
    return render_template('statistics.html',
                           wins=current_user.wins, draws=current_user.draws, loses=current_user.loses)


if __name__ == '__main__':
    app.run()
