import uuid

import boto3
import pytest
from fastapi import status
from moto import mock_aws
from starlette.testclient import TestClient

from main import app
from models import Brand
from store import BrandStore


@pytest.fixture
def client():
    return TestClient(app)


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


def test_get_brands(dynamodb_table):
    repository = BrandStore(table_name=dynamodb_table)

    brand = Brand.create(uuid.uuid4(), "test-brand")

    repository.add(brand)

    results = repository.list_open()

    assert results == [brand]
