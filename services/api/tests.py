import uuid

import boto3
import jwt
import pytest
from fastapi import status
from moto import mock_aws
from starlette.testclient import TestClient

from main import app, get_brand_store
from models import Brand
from store import BrandStore


@pytest.fixture
def brand_store(dynamodb_table):
    return BrandStore(dynamodb_table)


@pytest.fixture
def client(brand_store):
    app.dependency_overrides[get_brand_store] = lambda: brand_store
    return TestClient(app)


@pytest.fixture
def user_email():
    return "bob@builder.com"


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
            ],
        )
        yield table_name


def test_create_brand(dynamodb_table):
    repository = BrandStore(table_name=dynamodb_table)

    brand = Brand.create(uuid.uuid4(), "test-brand")

    repository.add(brand)

    result = repository.get_by_id(brand_id=brand.id, name=brand.name)

    assert result == brand


def test_create_brand_from_api(client, id_token):
    brand_data = {"name": "test-brand"}

    response = client.post(
        "/api/brands/", json=brand_data, headers={"Authorization": id_token}
    )

    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in body
    assert body["name"] == brand_data["name"]


def test_get_brands(dynamodb_table):
    repository = BrandStore(table_name=dynamodb_table)

    brand = Brand.create(uuid.uuid4(), "test-brand")

    repository.add(brand)

    results = repository.list_all()

    assert results == [brand]


def test_get_brands_from_api(client, user_email, id_token):
    brand_name = "sex wax"

    client.post(
        "/api/brands/", json={"name": brand_name}, headers={"Authorization": id_token}
    )

    response = client.get("/api/brands/", headers={"Authorization": id_token})

    body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert body["results"][0]["id"]
    assert body["results"][0]["name"] == brand_name
