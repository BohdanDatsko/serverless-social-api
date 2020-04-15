import json
import logging
import os
import uuid

import boto3

db = boto3.resource("dynamodb")


def create(event, context):
    if event:
        data = json.loads(event["body"])
        if "username" not in data:
            logging.error("Validation Failed")
            return {"statusCode": 500, "errorMassage": "Couldn't create the user item."}
        try:
            table = db.Table(os.environ["DYNAMODB_TABLE"])
            user_uuid = uuid.uuid1()
            item = {
                "id": f"{user_uuid}",
                "username": data["username"],
                "email": data["email"],
                "address": data["address"],
            }
            table.put_item(Item=item)  # write the item to the database
            response = {"statusCode": 200, "user_uuid": f"{user_uuid}"}  # create a response
            return response
        except Exception as e:
            return {"statusCode": 500, "errorMassage": logging.error(f"{e}")}
    else:
        return {"statusCode": 500, "errorMassage": "There isn't any body in data"}
