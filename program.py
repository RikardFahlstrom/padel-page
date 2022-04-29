from uuid import uuid4

from decouple import config
from flask import Flask, redirect, render_template, request, url_for

from dynamodb_handler import (
    add_game,
    get_dynamodb_resource,
    get_game,
    query_upcoming_games,
    update_players_in_db,
)
from utils import GameInfo, get_final_names, get_todays_date

app = Flask(__name__)
PASSPHRASE = config("PASSPHRASE_TO_POST")


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/view_games", methods=["GET"])
def view_games():
    dynamodb_resource = get_dynamodb_resource()
    upcoming_games = query_upcoming_games(dynamodb_resource)
    upcoming_games = [GameInfo(**game) for game in upcoming_games]
    upcoming_games_sorted = sorted(upcoming_games, key=lambda x: x.date)
    return render_template(
        "view_games.html", games=upcoming_games_sorted, todays_date=get_todays_date()
    )


@app.route("/add_game", methods=["GET", "POST"])
def add_new_game():
    if request.method == "POST":
        form_data = request.form.to_dict()
        if form_data.get("passphrase") == PASSPHRASE:
            form_data["id"] = str(uuid4())
            dynamodb_resource = get_dynamodb_resource()
            add_game(dynamo_resource=dynamodb_resource, game=form_data)
            return redirect(url_for("view_games"))

    return render_template("add_game.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/edit_game/<game_id>", methods=["GET"])
def edit(game_id):
    return render_template("edit.html", id_to_edit=game_id)


@app.route("/update_players", methods=["POST"])
def update_players():
    if request.method == "POST":
        updated_player_info = request.form.to_dict()
        dynamodb_resource = get_dynamodb_resource()
        current_player_info = get_game(
            dynamo_resource=dynamodb_resource,
            game_id=updated_player_info.get("game_id"),
        )
        final_player_names = get_final_names(current_player_info, updated_player_info)
        if updated_player_info.get("passphrase") == PASSPHRASE:
            update_players_in_db(
                dynamo_resource=dynamodb_resource,
                game_id=updated_player_info.get("game_id"),
                final_names=final_player_names,
            )

    return redirect(url_for("view_games"))


if __name__ == "__main__":
    app.run(debug=True)
