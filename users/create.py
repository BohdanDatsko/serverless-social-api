import json
import logging
import os
import uuid

import boto3

db = boto3.resource("dynamodb")


def create(event, context):
    if event:
        """To test locally run 
        serverless invoke local --function create --data
        '{"body": {"username": "Sirius Black", "email": "snuffles@gryffindor.com", "address": "13 Grymo Sq."}}'"""
        # data = event["body"]  # locally
        data = json.loads(event["body"])  # remote (AWS)
        if "username" not in data:
            logging.error("Validation Failed")
            err = {"errorMessage": "Couldn't create the user item."}
            return {"statusCode": 500, "body": json.dumps(err)}
        try:
            table = db.Table(os.environ["USERS_TABLE"])
            user_uuid = uuid.uuid1()
            item = {
                "id": f"{user_uuid}",
                "username": data["username"],
                "email": data["email"],
                "address": data["address"],
            }
            table.put_item(Item=item)  # write the item to the database
            response = {"statusCode": 201, "body": json.dumps(str(f"{user_uuid}"))}  # create a response
            return response
        except Exception as e:
            err = {"errorMessage": logging.error(f"{e}")}
            return {"statusCode": 500, "body": json.dumps(err)}
    else:
        err = {"errorMessage": "There isn't any body in data."}
        return {"statusCode": 500, "body": json.dumps(err)}
