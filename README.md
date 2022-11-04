# Padel Planner
*Add upcoming slots and let players add themselves to suitable slots for easier scheduling, add stats afterwards!*

---

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Visual Studio](https://img.shields.io/badge/Visual%20Studio-5C2D91.svg?style=for-the-badge&logo=visual-studio&logoColor=white)

## Installation
Clone the repository and add the following `.env` file to the root directory:


```bash
DEV_ENVIRONMENT='development' or 'production'
ROLLBAR_ACCESS_TOKEN='123abc'
SECRET_KEY='123cba'
SQLALCHEMY_DATABASE_URI='sqlite:///db/project.db'
SQLALCHEMY_ECHO=True
```

## <a name="title1"></a> Deploy webpage
Change to the directory containing the Dockerfile and run:
```bash
sudo docker build -t flask/padel-planner .
```
```bash
sudo docker run -d -p 8003:8000 --restart unless-stopped --mount type=bind,source="$(pwd)/db",target="/app/db" --name padel-planner-prod flask/padel-planner
```
Make sure to give the `/db` folder and its content read-write access by running `chmod -R 777 db/`.

## Deploy nginx and certbot

Clone this repository and follow instructions
https://github.com/wmnnd/nginx-certbot

Since I run the nginx-certbot container on the same host as the `flask/padel planner` container, I need to update the
nginx config file `data/nginx/app.conf` to redirect https to the container port on the server `<server-ip>:8003`.

## Setup development environment

Get a ready-to-use environment by opening the project as a [development container in VS Code](https://code.visualstudio.com/docs/devcontainers/containers).

Once the development container is opened, change directory to `src/padel-page` and run `python application.py` to run the Flask application.

## Add some basic data to the SQLite database
Change directory to `padel-page/src/padel-page/db` and run below scripts

Add courts specific to Uppsala
```bash
sqlite3 project.db "insert into arenas (name) values ('UTK'), ('Evry Padel Fyrislund'), ('Evry Padel Librobäck'), ('WAP Uppsala'), ('Uppsala Padel World'), ('City Padel: Uppsala'), ('USIF Arena'), ('-- select arena --');"
```
Add default leagues
```bash
sqlite3 project.db "insert into leagues (name) values ('average-joes'), ('justice-league'), ('too-poor-to-golf'), ('best-of-the-rest'), ('call-of-duty'), ('-- select league --');"
```
Add default players
```bash
sqlite3 project.db "insert into users (username) values ('zbackup-leonardo'), ('zbackup-raphael'), ('zbackup-donatello'), ('zbackup-michelangelo');"
```
Add some previous and upcoming games
```bash
sqlite3 project.db """
    insert into games
        (date, start_time, end_time, arena_id, league_id)
    values
        ('2021-05-01', '18:00:00', '20:00:00', '1', '2'),
        ('2023-06-10', '18:30:00', '20:30:00', '4', '1'),
        ('2022-06-11', '19:00:00', '22:00:00', '2', '2'),
        ('2022-11-01', '18:00:00', '20:00:00', '7', '4'),
        ('2023-01-22', '20:00:00', '22:15:00', '7', '4'),
        ('2023-06-04', '18:00:00', '20:00:00', '2', '5'),
        ('2023-11-10', '18:00:00', '20:00:00', '2', '5')
    ;"""
```
Add players to previous and upcoming games
```bash
sqlite3 project.db """
    insert into players
        (game_id, player_id)
    values
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (6, 4),
        (6, 3),
        (6, 2),
        (6, 1),
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 4)
    ;"""
```

:tennis: :calendar: :bar_chart:
