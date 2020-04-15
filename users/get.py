import logging
import os
import json

import boto3

db = boto3.resource("dynamodb")


def get(event, context):
    try:
        table = db.Table(os.environ["DYNAMODB_TABLE"])
        result = table.get_item(Key={"id": event["pathParameters"]["id"]})
        response = {"statusCode": 200, "body": json.dumps(result["Item"])}
        return response
    except Exception as e:
        return {"statusCode": 500, "errorMassage": logging.error(f"{e}")}
