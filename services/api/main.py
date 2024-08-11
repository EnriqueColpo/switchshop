from typing import Union

import jwt
from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette import status

from config import Config
from models import ProductInventory
from schemas import (CreateProductInventorySchema, ProductInventoryListSchema,
                     ProductInventoryResponseSchema, ProductInventorySchema)
from stores.product_inventory_store import ProductInventoryStore

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = Config()


def get_product_inventory_store():
    return ProductInventoryStore(config.TABLE_NAME, config.DYNAMODB_URL)


def get_user_email(Authorization: Union[bytes, None] = Header(default=None)) -> str:
    print(Authorization)
    user_object = jwt.decode(Authorization, options={"verify_signature": False})
    return user_object["cognito:username"]


@app.get("/api/health-check/")
def health_check():
    return {"message": "OK"}


@app.post(
    "/api/product_inventory/",
    response_model=ProductInventorySchema,
    status_code=status.HTTP_201_CREATED,
)
def create_product_inventory(
    parameters: CreateProductInventorySchema,
    user_email: str = Depends(get_user_email),
    product_inventory_store: ProductInventoryStore = Depends(
        get_product_inventory_store
    ),
):
    product_inventory = ProductInventory.create(
        parameters.product_name,
        parameters.location_id,
        parameters.category_name,
        parameters.brand_name,
        parameters.description,
        parameters.price,
        parameters.total_stock_quantity,
        parameters.last_restock_date,
        parameters.inventory,
    )
    product_inventory_store.add(product_inventory)
    return product_inventory


@app.get(
    "/api/product_inventory/{product_inventory_id}/{location_id}",
    response_model=ProductInventoryResponseSchema,
)
def get_product_inventory(
    product_inventory_id: str,
    location_id: str,
    user_email: str = Depends(get_user_email),
    product_inventory_store: ProductInventoryStore = Depends(
        get_product_inventory_store
    ),
):
    response = product_inventory_store.get_by_id(product_inventory_id, location_id)
    response = ProductInventoryResponseSchema(result=response.__dict__)
    print(response)
    return response


@app.get("/api/product_inventory/", response_model=ProductInventoryListSchema)
def get_product_inventory_list(
    category_name: str = None,
    brand_name: str = None,
    user_email: str = Depends(get_user_email),
    product_inventory_store: ProductInventoryStore = Depends(
        get_product_inventory_store
    ),
):
    response = product_inventory_store.filter(category_name, brand_name)
    return ProductInventoryListSchema(results=response)


handle = Mangum(app)
