import datetime

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decouple import config

from utils import GameInfoStore

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")
TABLE_NAME = config("TABLE_NAME")


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
    )


def create_game_table(dynamo_resource):
    return dynamo_resource.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )


def get_game(dynamo_resource, game_id):
    table = dynamo_resource.Table(TABLE_NAME)

    try:
        response = table.get_item(Key={"id": game_id})
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return response["Item"]


def add_game(dynamo_resource, game):
    game_info_to_add = GameInfoStore(**game)
    table = dynamo_resource.Table(TABLE_NAME)
    print(f"Adding game: {game_info_to_add.dict()}")
    table.put_item(Item=game_info_to_add.dict())


def query_upcoming_games(dynamo_resource):
    table = dynamo_resource.Table(TABLE_NAME)

    scan_kwargs = {
        "FilterExpression": Key("date").gte(datetime.date.today().strftime("%Y-%m-%d")),
    }

    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs["ExclusiveStartKey"] = start_key
        response = table.scan(**scan_kwargs)
        start_key = response.get("LastEvaluatedKey", None)
        done = start_key is None

    return response["Items"]


def update_players_in_db(dynamo_resource, game_id, final_names):
    table = dynamo_resource.Table(TABLE_NAME)

    return table.update_item(
        Key={
            "id": game_id,
        },
        UpdateExpression="set player1=:r, player2=:p, player3=:a, player4=:g",
        ExpressionAttributeValues={
            ":r": final_names.get("player1"),
            ":p": final_names.get("player2"),
            ":a": final_names.get("player3"),
            ":g": final_names.get("player4"),
        },
        ReturnValues="UPDATED_NEW",
    )


if __name__ == "__main__":
    dynamodb_resource = get_dynamodb_resource()
    existing_tables = dynamodb_resource.meta.client.list_tables()["TableNames"]
    print(f"Existing tables: {existing_tables}")

    if TABLE_NAME not in existing_tables:
        game_table = create_game_table(dynamo_resource=dynamodb_resource)
    upcoming_games = query_upcoming_games(dynamo_resource=dynamodb_resource)
    print(f"Upcoming games: {upcoming_games}")
