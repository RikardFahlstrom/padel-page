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
```

## Deploy webpage
```bash
docker build -t flask/padel-planner .
```
```bash
docker run -d -p 8003:8000 --restart unless-stopped flask/padel-planner
```


## Deploy nginx
```bash
docker build -t nginx .
```
```bash
docker run -d -p 80:80 --restart unless-stopped --add-host=host.docker.internal:host-gateway nginx
```

Flag `--add-host=host.docker.internal:host-gateway` is needed to deploy in Linux, not needed on Mac.

---

:tennis: :calendar: :bar_chart:
