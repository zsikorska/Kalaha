from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('start.html')
    else:
        return redirect('/sign_in')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.route('/create_account')
def create_account():
    return render_template('create_account.html')


@app.route('/game')
def play():
    return render_template('game.html')


if __name__ == '__main__':
    app.run()
