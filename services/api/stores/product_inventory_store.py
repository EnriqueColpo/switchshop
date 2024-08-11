import boto3
from boto3.dynamodb.conditions import Key
from models import ProductInventory


class ProductInventoryStore:
    def __init__(self, table_name, dynamodb_url=None):
        self.table_name = table_name
        self.dynamodb_url = dynamodb_url

    def add(self, product_inventory):
        dynamodb = boto3.resource("dynamodb", endpoint_url=self.dynamodb_url)
        table = dynamodb.Table(self.table_name)
        table.put_item(Item={**product_inventory.__dict__})

    def get_by_id(self, product_inventory_id, location_id):
        dynamodb = boto3.resource("dynamodb", endpoint_url=self.dynamodb_url)
        table = dynamodb.Table(self.table_name)

        record = table.get_item(
            Key={
                "PK": f"PRODUCT#{product_inventory_id}",
                "SK": f"LOCATION#{location_id}",
            },
        )

        return ProductInventory(
            PK=record["Item"]["PK"],
            SK=record["Item"]["SK"],
            GS1PK=record["Item"]["GS1PK"],
            GS1SK=record["Item"]["GS1SK"],
            GS2PK=record["Item"]["GS2PK"],
            GS2SK=record["Item"]["GS2SK"],
            GS3PK=record["Item"]["GS3PK"],
            GS3SK=record["Item"]["GS3SK"],
            ProductName=record["Item"]["ProductName"],
            LocationId=record["Item"]["LocationId"],
            CategoryName=record["Item"]["CategoryName"],
            BrandName=record["Item"]["BrandName"],
            Description=record["Item"]["Description"],
            Price=record["Item"]["Price"],
            TotalStockQuantity=record["Item"]["TotalStockQuantity"],
            LastRestockDate=record["Item"]["LastRestockDate"],
            Inventory=record["Item"]["Inventory"],
        )

    def filter(self, category_name=None, brand_name=None):
        if category_name:
            response = self.get_by_category(category_name)
        elif brand_name:
            response = self.get_by_brand(brand_name)

        return response

    def get_by_category(self, category_name):
        dynamodb = boto3.resource("dynamodb", endpoint_url=self.dynamodb_url)
        table = dynamodb.Table(self.table_name)

        response = table.query(
            IndexName="GS1",
            KeyConditionExpression=Key("GS1PK").eq(f"CATEGORY#{category_name}"),
        )

        return response["Items"]

    def get_by_brand(self, brand_name):
        dynamodb = boto3.resource("dynamodb", endpoint_url=self.dynamodb_url)
        table = dynamodb.Table(self.table_name)

        response = table.query(
            IndexName="GS2",
            KeyConditionExpression=Key("GS2PK").eq(f"BRAND#{brand_name}"),
        )

        return response["Items"]
