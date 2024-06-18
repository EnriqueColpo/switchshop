import uuid
from typing import Union

import jwt
from fastapi import Depends, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette import status

from config import Config
from models import Brand
from schemas import APIBrand, APIBrandList, CreateBrand
from store import BrandStore

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = Config()


def get_brand_store():
    return BrandStore(config.TABLE_NAME, config.DYNAMODB_URL)


def get_user_email(authorization: Union[str, None] = Header(default=None)) -> str:
    print(authorization)
    user_object = jwt.decode(authorization, options={"verify_signature": False})
    return user_object["cognito:username"]


@app.get("/api/health-check/")
def health_check():
    return {"message": "OK"}


@app.post("/api/brands/", response_model=APIBrand, status_code=status.HTTP_201_CREATED)
def create_brand(
    parameters: CreateBrand,
    user_email: str = Depends(get_user_email),
    brand_store: BrandStore = Depends(get_brand_store),
):
    brand = Brand.create(uuid.uuid4(), parameters.name)
    brand_store.add(brand)
    return brand


@app.get("/api/brands/", response_model=APIBrandList)
def get_brands(
    user_email: str = Depends(get_user_email),
    brand_store: BrandStore = Depends(get_brand_store),
):
    response = brand_store.list_all()
    response = [brand.__dict__ for brand in response]
    return APIBrandList(results=response)


handle = Mangum(app)
