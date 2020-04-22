import logging
import os
import json

import boto3

dynamodb = boto3.resource("dynamodb")


def get(event, context):
    try:
        table = dynamodb.Table(os.environ["SOCIAL_APP_TABLE"])
        result = table.get_item(Key={"id": event["pathParameters"]["id"]})
        response = {"statusCode": 200, "body": json.dumps(result["Item"])}
        return response
    except Exception as e:
        err = {"errorMassage": logging.error(f"{e}")}
        return {"statusCode": 500, "body": json.dumps(err)}
