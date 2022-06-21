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
# function should take the str ID of a user, and returns the corresponding user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# function renders a start page template
# if user is authenticated, he is redirected to his home page
@app.route('/')
def start():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('start.html')


# function renders a page for sign in
# if user is authenticated, he is redirected to his home page
# method 'POST' checks users login and password and redirects to users home page or displays proper message
@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        nick = request.form['nick']
        password = request.form['password']

        user = User.query.filter_by(nick=nick).first()  # retrieve a user by nick

        if user is None:
            flash(f"User with the nick {nick} does not exist.")
            return redirect('/sign_in')

        elif bcrypt.check_password_hash(user.password, password):  # checking hashed password
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


# function renders a page for creating account
# if user is authenticated, he is redirected to his home page
# method 'POST' checks if user exist in base and redirects to users home page or displays proper message
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


# logout the user, stops game if running, refreshes the board and redirects to start page
@app.route('/sign_out')
@login_required
def sign_out():
    global running_game

    board.refresh()
    running_game = False
    logout_user()
    return redirect('/')


# global variables
board = Board()
first_player = True  # True if is the turn of player1, False if player2
ai = AIPlayer(False)
mode = 'human'
running_game = False
user_starts = True  # True if user is player1 (he begins the game), False if player2


# Function displays board, players can click proper button in order to move from specific house
# if end of game statistics are updated and user is redirected to results
@app.route('/game', methods=["GET", "POST"])
@login_required
def play_with_human():
    global first_player
    global mode
    global running_game

    if request.method == 'POST':
        house = int(request.form['house'])
        code = board.move(house, first_player)

        match code:
            case 0:  # change of players
                first_player = not first_player
                return redirect('/game')
            case 1:  # additional move
                return redirect('/game')
    else:
        mode = 'human'
        if board.is_end_of_game(first_player):
            board.end_of_game(first_player)
            update_statistics()
            running_game = False
            return redirect('/results')
        return render_template('board.html', moves=board.possible_moves(first_player), board=board.board)


# Function displays board, user can click proper button in order to move from specific house
# if is AI turn the proper function is called
# if end of game statistics are updated and user is redirected to results
@app.route('/gameAI', methods=["GET", "POST"])
@login_required
def play_with_ai():
    global mode
    global running_game

    if request.method == 'POST':
        house = int(request.form['house'])
        code = board.move(house, user_starts)

        match code:
            case 0:  # change of players
                return ai_move()
            case 1:  # additional move
                return redirect('/gameAI')
    else:
        mode = 'ai'
        if board.is_end_of_game(user_starts):
            board.end_of_game(user_starts)
            update_statistics()
            running_game = False
            return redirect('/results')
        return render_template('board.html', moves=board.possible_moves(user_starts), board=board.board)


# Function responsible for making AI move
# if end of game statistics are updated and user is redirected to results
def ai_move():
    global running_game

    if board.is_end_of_game(ai.first):
        board.end_of_game(ai.first)
        update_statistics()
        running_game = False
        return redirect('/results')

    house = ai.make_move(board)
    code = board.move(house, ai.first)

    match code:
        case 0:     # change of players
            return redirect('/gameAI')
        case 1:     # additional move
            return ai_move()


# Function displays home page, user can choose the settings of the game and after submitting redirected to game page
@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    global first_player
    global running_game
    global user_starts

    if request.method == 'POST':
        # play with other human
        if request.form['play'] == 'human':
            board.refresh()
            running_game = True
            first_player = True
            user_starts = (int(request.form['player']) == 1)        # which player the user wants to be
            return redirect('/game')

        # play with AI
        elif request.form['play'] == 'ai':
            board.refresh()
            running_game = True
            first_player = True
            user_starts = (int(request.form['player']) == 1)        # which player the user wants to be
            ai.first = not user_starts
            ai.level = int(request.form['ai level'])                # set the level of AI

            if user_starts:
                return redirect('/gameAI')
            else:
                return ai_move()

        # resume game (with human with previous settings)
        elif mode == 'human':
            return redirect('/game')

        # resume game (with AI with previous settings)
        else:
            return redirect('/gameAI')

    else:
        return render_template('home.html', resume=running_game)


# Function displays results
# if user wants to play again, he is redirected to game page with the same settings
# if not, he is redirected to his home page
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


# Function updates the data about wins, draws and loses of the user in the database
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


# Function displays statistics
@app.route('/statistics', methods=["GET", "POST"])
@login_required
def statistics():
    return render_template('statistics.html',
                           wins=current_user.wins, draws=current_user.draws, loses=current_user.loses)


if __name__ == '__main__':
    app.run()
