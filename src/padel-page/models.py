from datetime import date, datetime

from decouple import config
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship("Player", backref="user")
    results = db.relationship("Result", backref="user")

    def __repr__(self):
        return "<User %r>" % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class League(db.Model):
    __tablename__ = "leagues"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    games = db.relationship("Game", backref="league")


class Arena(db.Model):
    __tablename__ = "arenas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True)

    games = db.relationship("Game", backref="arena")


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False, index=True)
    end_time = db.Column(db.Time, nullable=False)
    arena_id = db.Column(db.Integer, db.ForeignKey(Arena.id), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey(League.id), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship("Player", backref="game")
    results = db.relationship("Result", backref="game")


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    player_id = db.Column(db.Integer, db.ForeignKey(User.id))


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=False)
    player_id = db.Column(db.String(120), db.ForeignKey(User.id))
    winner = db.Column(db.Boolean)
