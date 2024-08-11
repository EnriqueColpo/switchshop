import os

import boto3

client = boto3.client("dynamodb", endpoint_url=os.getenv("DYNAMODB_URL"))
table_name = os.getenv("TABLE_NAME")
client.create_table(
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "GS1PK", "AttributeType": "S"},
        {"AttributeName": "GS1SK", "AttributeType": "S"},
        {"AttributeName": "GS2PK", "AttributeType": "S"},
        {"AttributeName": "GS2SK", "AttributeType": "S"},
        {"AttributeName": "GS3PK", "AttributeType": "S"},
        {"AttributeName": "GS3SK", "AttributeType": "S"},
    ],
    TableName=table_name,
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    BillingMode="PAY_PER_REQUEST",
    GlobalSecondaryIndexes=[
        {
            "IndexName": "GS1",
            "KeySchema": [
                {"AttributeName": "GS1PK", "KeyType": "HASH"},
                {"AttributeName": "GS1SK", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        },
        {
            "IndexName": "GS2",
            "KeySchema": [
                {"AttributeName": "GS2PK", "KeyType": "HASH"},
                {"AttributeName": "GS2SK", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        },
        {
            "IndexName": "GS3",
            "KeySchema": [
                {"AttributeName": "GS3PK", "KeyType": "HASH"},
                {"AttributeName": "GS3SK", "KeyType": "RANGE"},
            ],
            "Projection": {
                "ProjectionType": "ALL",
            },
        },
    ],
)
