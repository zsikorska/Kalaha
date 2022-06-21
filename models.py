from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# table with data of users: data for authentication and statistics
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    draws = db.Column(db.Integer, nullable=False)
    loses = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.nick
