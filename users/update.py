import json
import logging
import os

import boto3

dynamodb = boto3.resource("dynamodb")


def update(event, context):
    if event:
        # data = event["body"]  # locally
        data = json.loads(event["body"])  # remote (AWS)
        if "id" not in data:
            logging.error("Validation Failed")
            raise Exception("Couldn't update the user item.")
        try:
            table = dynamodb.Table(os.environ["SOCIAL_APP_TABLE"])
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
            err = {"errorMassage": logging.error(f"{e}")}
            return {"statusCode": 500, "body": json.dumps(err)}
    else:
        err = {"errorMassage": "There isn't any body in data"}
        return {"statusCode": 500, "body": json.dumps(err)}
