import boto3
import uuid

db = boto3.resource("dynamodb")


def follow_user(followed_user, following_user):
    user = f"USER#{followed_user}"
    friend = f"#FRIEND#{following_user}"
    user_metadata = f"#METADATA#{followed_user}"
    friend_user = f"USER#{following_user}"
    friend_metadata = f"#METADATA#{following_user}"
    try:
        resp = db.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "serverless-social-api-dev",
                        "Item": {
                            "PK": {"S": user},
                            "SK": {"S": friend},
                            "followedUser": {"S": followed_user},
                            "followingUser": {"S": following_user},
                        },
                        "ConditionExpression": "attribute_not_exists(SK)",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                    }
                },
                {
                    "Update": {
                        "TableName": "serverless-social-api-dev",
                        "Key": {"PK": {"S": user}, "SK": {"S": user_metadata}},
                        "UpdateExpression": "SET followers = followers + :i",
                        "ExpressionAttributeValues": {":i": {"N": "1"}},
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                    }
                },
                {
                    "Update": {
                        "TableName": "serverless-social-api-dev",
                        "Key": {"PK": {"S": friend_user}, "SK": {"S": friend_metadata}},
                        "UpdateExpression": "SET following = following + :i",
                        "ExpressionAttributeValues": {":i": {"N": "1"}},
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                    }
                },
            ]
        )
        print(f"User {following_user} is now following user {followed_user}")
        return True
    except Exception as e:
        print(e)
        print("Could not add follow relationship")
