from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('start.html')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


if __name__ == '__main__':
    app.run()
