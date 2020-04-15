import json
import logging
import os

import boto3

db = boto3.resource("dynamodb")


def update(event, context):
    if event:
        data = json.loads(event["body"])
        if "id" not in data:
            logging.error("Validation Failed")
            raise Exception("Couldn't update the user item.")
        try:
            table = db.Table(os.environ["DYNAMODB_TABLE"])
            result = table.update_item(
                Key={"id": event["pathParameters"]["id"]},
                ExpressionAttributeNames={"#username": "username"},
                ExpressionAttributeValues={
                    ":username": data["username"],
                    ":email": data["email"],
                    ":address": data["address"],
                },
                UpdateExpression="SET #username = :username, "
                "email = :email, "
                "address = :address",
                ReturnValues="ALL_NEW",
            )
            response = {"statusCode": 200, "body": json.dumps(result["Attributes"])}
            return response
        except Exception as e:
            return {"statusCode": 500, "errorMassage": logging.error(f"{e}")}
    else:
        return {"statusCode": 500, "errorMassage": "There isn't any body in data"}
