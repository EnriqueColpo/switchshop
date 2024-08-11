from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ProductInventorySchema(BaseModel):
    PK: str
    SK: str
    GS1PK: str
    GS1SK: str
    GS2PK: str
    GS2SK: str
    GS3PK: str
    GS3SK: str
    ProductName: str
    LocationId: str
    CategoryName: str
    BrandName: str
    Description: str
    Price: int
    TotalStockQuantity: int
    LastRestockDate: str
    Inventory: List[dict]

    class ConfigDict:
        orm_mode = True


class ProductInventoryListSchema(BaseModel):
    results: List[ProductInventorySchema]

    class ConfigDict:
        orm_mode = True


class ProductInventoryResponseSchema(BaseModel):
    result: ProductInventorySchema

    class ConfigDict:
        orm_mode = True


class CreateProductInventorySchema(BaseModel):
    product_name: str
    location_id: str
    category_name: str
    brand_name: str
    description: str
    price: int
    total_stock_quantity: int
    last_restock_date: str
    inventory: List[dict]

    class ConfigDict:
        orm_mode = True


class ProductInventoryFilter(BaseModel):
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    location_id: Optional[str] = None
