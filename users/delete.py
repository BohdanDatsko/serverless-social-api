import logging
import os

import boto3

db = boto3.resource("dynamodb")


def delete(event, context):
    try:
        table = db.Table(os.environ["DYNAMODB_TABLE"])
        table.delete_item(Key={"id": event["pathParameters"]["id"]})
        response = {"statusCode": 200}
        return response
    except Exception as e:
        return {"statusCode": 500, "errorMassage": logging.error(f"{e}")}
