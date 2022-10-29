import datetime
import os
from ast import alias
from crypt import methods
from uuid import uuid4

import rollbar
import rollbar.contrib.flask
from decouple import config
from flask import (
    Flask,
    flash,
    got_request_exception,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_bootstrap import Bootstrap
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from forms import GameForm, LoginForm, RegistrationForm, StatForm
from sqlalchemy import func
from utils import GameInfo, get_final_names, get_todays_date
from werkzeug.urls import url_parse

app = Flask(__name__)
app.secret_key = config("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

from models import Arena, Game, League, Player, Result, User, db

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


bootstrap = Bootstrap(app)


environment = config("DEV_ENVIRONMENT")
rollbar_token = config("ROLLBAR_ACCESS_TOKEN")


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_token,
        # environment name
        environment,
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False,
    )

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/view_games", methods=["GET"])
@login_required
def view_games():
    games = (
        db.session.query(Game)
        .filter(Game.date >= datetime.date.today())
        .order_by(Game.date, Game.start_time)
    )
    return render_template(
        "view_games.html", title="Upcoming", games=games, todays_date=get_todays_date()
    )


@app.route("/add_game", methods=["GET", "POST"])
@login_required
def add_game():
    form = GameForm()
    form.players.choices = sorted([user.username for user in User.query.all()])
    form.arena.choices = sorted([arena.name for arena in Arena.query.all()])
    form.league.choices = sorted([league.name for league in League.query.all()])

    if form.validate_on_submit():
        selected_arena_id = db.session.execute(
            db.select(Arena.id).filter_by(name=form.arena.data)
        ).one()
        selected_league_id = db.session.execute(
            db.select(League.id).filter_by(name=form.league.data)
        ).one()

        game = Game(
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            arena_id=selected_arena_id[0],
            league_id=selected_league_id[0],
        )
        db.session.add(game)
        db.session.commit()

        last_added_game = db.session.execute(
            db.select(Game.id).order_by(Game.id.desc())
        ).first()

        player1 = Player(
            game_id=game.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[0])
            ).scalar(),
        )
        player2 = Player(
            game_id=game.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[1])
            ).scalar(),
        )
        player3 = Player(
            game_id=game.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[2])
            ).scalar(),
        )
        player4 = Player(
            game_id=game.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[3])
            ).scalar(),
        )
        db.session.add(player1)
        db.session.add(player2)
        db.session.add(player3)
        db.session.add(player4)

        db.session.commit()
        flash("Game added!")
        return redirect(url_for("view_games"))

    return render_template("add_game.html", title="Add game", form=form)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    form = GameForm()
    form.players.choices = sorted([user.username for user in User.query.all()])
    form.arena.choices = sorted([arena.name for arena in Arena.query.all()])
    form.league.choices = sorted([league.name for league in League.query.all()])

    game_info = Game.query.filter_by(id=game_id).first()
    if form.validate_on_submit():
        new_arena_id = db.session.execute(
            db.select(League.id).filter_by(name=form.league.data)
        ).one()
        new_league_id = db.session.execute(
            db.select(League.id).filter_by(name=form.league.data)
        ).one()
        game_info.date = form.date.data
        game_info.start_time = form.start_time.data
        game_info.end_time = form.end_time.data
        game_info.arena_id = new_arena_id[0]
        game_info.league_id = new_league_id[0]

        Player.query.filter_by(game_id=game_info.id).delete()
        db.session.commit()

        player1 = Player(
            game_id=game_info.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[0])
            ).scalar(),
        )
        player2 = Player(
            game_id=game_info.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[1])
            ).scalar(),
        )
        player3 = Player(
            game_id=game_info.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[2])
            ).scalar(),
        )
        player4 = Player(
            game_id=game_info.id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.players.data[3])
            ).scalar(),
        )
        db.session.add(player1)
        db.session.add(player2)
        db.session.add(player3)
        db.session.add(player4)

        db.session.commit()
        flash(
            f"You have successfully updated the information for game id {game_info.id}"
        )
        return redirect(url_for("view_games"))
    return render_template(
        "edit_game.html",
        title="Edit",
        id_to_edit=game_id,
        form=form,
        current_info=game_info,
    )


@app.route("/add_stats/<game_id>", methods=["GET", "POST"])
@login_required
def add_stats(game_id):
    form = StatForm()
    game_info = Game.query.filter_by(id=game_id).first()
    players = sorted([player.user.username for player in game_info.players])

    form.winners.choices = players
    form.losers.choices = players

    if form.validate_on_submit():
        result = Result(
            game_id=game_id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.winners.data[0])
            ).scalar(),
            winner=True,
        )
        db.session.add(result)

        result = Result(
            game_id=game_id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.winners.data[1])
            ).scalar(),
            winner=True,
        )
        db.session.add(result)

        result = Result(
            game_id=game_id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.losers.data[0])
            ).scalar(),
            winner=False,
        )
        db.session.add(result)

        result = Result(
            game_id=game_id,
            player_id=db.session.execute(
                db.select(User.id).filter_by(username=form.losers.data[1])
            ).scalar(),
            winner=False,
        )
        db.session.add(result)

        db.session.commit()

        flash("Stats registered!")
        return redirect(url_for("view_stats"))

    return render_template(
        "add_stats.html", title="Add stats", game_info=game_info, form=form
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/stats")
@login_required
def stats():
    previous_games = db.session.execute(
        db.select(Game).filter(Game.date <= datetime.date.today()).order_by(Game.date)
    ).scalars()
    return render_template("stats.html", title="Stats", previous_games=previous_games)


@app.route("/view_stats")
@login_required
def view_stats():
    total_games = db.session.query(Game).count()
    top_3_players = (
        db.session.query(Result, func.count(func.distinct(Result.game_id)))
        .filter(Result.winner == True)
        .join(User)
        .group_by(User.username)
        .order_by(func.count(func.distinct(Result.game_id)).desc())
        .all()
    )
    return render_template(
        "view_stats.html",
        title="View stats",
        total_games=total_games,
        top_3_players=top_3_players,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_leagues = None
    upcoming_games = Player.query.filter(Player.player_id == user.id).all()

    return render_template(
        "profile.html",
        title="Profile",
        user=user,
        user_leagues=user_leagues,
        upcoming_games=upcoming_games,
    )


if __name__ == "__main__":
    app.run(debug=True)
