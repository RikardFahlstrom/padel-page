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
AWS_ACCESS_KEY_ID='your_access_key_id'
AWS_SECRET_ACCESS_KEY='your_secret_access_key'
REGION_NAME='aws-region'
TABLE_NAME='dynamodb-tablename'
PASSPHRASE_TO_POST='passphrase'
DEV_ENVIRONMENT='development' or 'production'
ROLLBAR_ACCESS_TOKEN='123abc'
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
