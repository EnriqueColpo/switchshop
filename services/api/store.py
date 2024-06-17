from uuid import UUID

import boto3

from models import Brand


class BrandStore:
    def __init__(self, table_name, dynamodb_url=None):
        self.table_name = table_name
        self.dynamodb_url = dynamodb_url

    def add(self, brand):
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=self.dynamodb_url
        )
        table = dynamodb.Table(self.table_name)
        table.put_item(
            Item={
                "PK": f"#{brand.name}",
                "SK": f"#{brand.id}",
                "id": str(brand.id),
                "name": brand.name,
            }
        )

    def get_by_id(self, brand_id, name):
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=self.dynamodb_url
        )
        table = dynamodb.Table(self.table_name)
        record = table.get_item(
            Key={
                "PK": f"#{name}",
                "SK": f"#{brand_id}",
            },
        )

        return Brand(
            id=UUID(record["Item"]["id"]),
            name=record["Item"]["name"],
        )

    def list_open(self):
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=self.dynamodb_url
        )

        table = dynamodb.Table(self.table_name)
        response = table.scan()

        results = [
            Brand(id=UUID(record["id"]), name=record["name"])
            for record in response["Items"]
        ]

        return results
