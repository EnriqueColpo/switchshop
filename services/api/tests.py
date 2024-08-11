import boto3
import jwt
import pytest
from fastapi import status
from moto import mock_aws
from starlette.testclient import TestClient

from main import app, get_product_inventory_store
from models import ProductInventory
from stores.product_inventory_store import ProductInventoryStore


@pytest.fixture
def product_inventory_store(dynamodb_table):
    return ProductInventoryStore(dynamodb_table)


@pytest.fixture
def client(product_inventory_store):
    app.dependency_overrides[get_product_inventory_store] = lambda: product_inventory_store
    return TestClient(app)


@pytest.fixture
def user_email():
    return "henry@karamazov.com"


@pytest.fixture
def id_token(user_email):
    return jwt.encode({"cognito:username": user_email}, "secret")


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/api/health-check/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK"}


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        client = boto3.client("dynamodb")
        table_name = "test-table"
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
        yield table_name


def test_create_product_inventory(dynamodb_table):
    repository = ProductInventoryStore(table_name=dynamodb_table)

    product_inventory = ProductInventory.create(
        product_name="Magazine",
        location_id="switch",
        category_name="T-Shirts",
        brand_name="Thrasher",
        description="Classic logo",
        price=25000,
        total_stock_quantity=1,
        last_restock_date="11/08/2024",
        inventory=[
            {
                "color": "black",
                "size": "XL",
                "quantity": "9",
                "description": "black like my soul"
            }
        ]
    )

    repository.add(product_inventory)

    print(product_inventory)

    result = repository.get_by_id(
        product_inventory_id=product_inventory.ProductName,
        location_id=product_inventory.LocationId
    )

    assert result == product_inventory


def test_create_product_inventory_from_api(client, id_token):
    product_inventory_data = {
        "product_name": "Magazine",
        "location_id": "switch",
        "category_name": "T-Shirts",
        "brand_name": "Thrasher",
        "description": "Classic logo",
        "price": 25000,
        "total_stock_quantity": 1,
        "last_restock_date": "11/08/2024",
        "inventory": [
            {
                "color": "black",
                "size": "XL",
                "quantity": "9",
                "description": "black like my soul"
            }
        ]
    }

    response = client.post(
        "/api/product_inventory/", json=product_inventory_data, headers={"Authorization": id_token}
    )

    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "PK" in body
    assert body["ProductName"] == product_inventory_data["product_name"]
    assert body["Inventory"] == product_inventory_data["inventory"]


def test_get_product_inventory(dynamodb_table):
    repository = ProductInventoryStore(table_name=dynamodb_table)

    product_inventory = ProductInventory.create(
        product_name="Magazine",
        location_id="switch",
        category_name="T-Shirts",
        brand_name="Thrasher",
        description="Classic logo",
        price=25000,
        total_stock_quantity=1,
        last_restock_date="11/08/2024",
        inventory=[
            {
                "color": "black",
                "size": "XL",
                "quantity": "9",
                "description": "black like my soul"
            }
        ]
    )

    repository.add(product_inventory)

    result = repository.get_by_id(
        product_inventory_id=product_inventory.ProductName,
        location_id=product_inventory.LocationId
    )

    assert result == product_inventory


def test_get_product_inventory_from_api(client, user_email, id_token):
    product_inventory_data = {
        "product_name": "Magazine",
        "location_id": "switch",
        "category_name": "T-Shirts",
        "brand_name": "Thrasher",
        "description": "Classic logo",
        "price": 25000,
        "total_stock_quantity": 1,
        "last_restock_date": "11/08/2024",
        "inventory": [
            {
                "color": "black",
                "size": "XL",
                "quantity": "9",
                "description": "black like my soul"
            }
        ]
    }

    client.post(
        "/api/product_inventory/", json=product_inventory_data, headers={"Authorization": id_token}
    )

    response = client.get("/api/product_inventory/Magazine/switch", headers={"Authorization": id_token})

    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["result"]["ProductName"]
    assert body["result"]["Inventory"] == product_inventory_data["inventory"]