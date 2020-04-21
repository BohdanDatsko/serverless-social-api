import json
import logging
import os

import boto3

db = boto3.resource("dynamodb")


def list(event, context):
    try:
        table = db.Table(os.environ["USERS_TABLE"])
        result = table.scan()
        response = {"statusCode": 200, "body": json.dumps(result["Items"])}
        return response
    except Exception as e:
        err = {"errorMassage": logging.error(f"{e}")}
        return {"statusCode": 500, "body": json.dumps(err)}
