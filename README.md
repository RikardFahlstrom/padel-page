# Padel Planner
*Add upcoming slots and let players add themselves to suitable slots for easier scheduling, add stats afterwards!*

---

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

## Installation
Clone the repository and add the following `.env` file to the root directory:


```bash
DEV_ENVIRONMENT='development' or 'production'
ROLLBAR_ACCESS_TOKEN='123abc'
SECRET_KEY='123cba'
SQLALCHEMY_DATABASE_URI='sqlite:///project.db'
```

## <a name="title1"></a> Deploy webpage
```bash
sudo docker build -t flask/padel-planner .
```
```bash
sudo docker run -d -p 8003:8000 --restart unless-stopped flask/padel-planner
```


## Deploy nginx and certbot

Clone this repository and follow instructions
https://github.com/wmnnd/nginx-certbot

Since I run the nginx-certbot container on the same host as the `flask/padel planner` container, I need to update the
nginx config file `data/nginx/app.conf` to redirect https to the container port on the server `<server-ip>:8003`.

## Setup development environment

Create a local in-memory dynamodb available on port `localhost:8001` by running
```bash
docker run -d -p 8001:8000 --rm --name my-dev-dynamodb amazon/dynamodb-local
```

Create a virtualenv and install requirements.txt

Run below command from top-level directory to create the dynamodb table and to add a game
```python
python dynamodb_handler.py
```

Do the steps under [Do deploy](#title1) to deploy the webpage and open [0.0.0.0:8003](http://0.0.0.0:8003/) in your browser!

:tennis: :calendar: :bar_chart:

```bash
sqlite3 project.db "insert into arenas (name) values ('UTK'), ('Evry Padel Fyrislund'), ('Evry Padel Librobäck'), ('WAP Uppsala'), ('Uppsala Padel World'), ('City Padel: Uppsala'), ('USIF Arena'), ('-- select arena --');"
sqlite3 project.db "insert into leagues (name) values ('average-joes'), ('justice-league'), ('too-poor-to-golf'), ('best-of-the-rest'), ('call-of-duty'), ('-- select league --');"
sqlite3 project.db "insert into users (username) values ('zbackup-leonardo'), ('zbackup-raphael'), ('zbackup-donatello'), ('zbackup-michelangelo');"
 sqlite3 project.db """
    insert into games
        (date, start_time, end_time, arena_id, league_id)
    values
        ('2022-05-01', '18:00:00', '20:00:00', '1', '2'),
        ('2023-06-10', '18:30:00', '20:30:00', '4', '1'),
        ('2022-06-11', '19:00:00', '22:00:00', '2', '2'),
        ('2022-11-01', '18:00:00', '20:00:00', '7', '4'),
        ('2022-11-22', '20:00:00', '22:15:00', '7', '4'),
        ('2023-01-04', '18:00:00', '20:00:00', '2', '5'),
        ('2023-01-10', '18:00:00', '20:00:00', '2', '5')
    ;"""

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
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 4)
    ;"""
```
