from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


@dataclass
class ProductInventory:
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

    @classmethod
    def create(
        cls,
        product_name,
        location_id,
        category_name,
        brand_name,
        description,
        price,
        total_stock_quantity,
        last_restock_date,
        inventory,
    ):
        pk = f"PRODUCT#{product_name}"
        sk = f"LOCATION#{location_id}"
        gs1pk = f"CATEGORY#{category_name}"
        gs1sk = f"PRODUCT#{product_name}"
        gs2pk = f"BRAND#{brand_name}"
        gs2sk = f"PRODUCT#{product_name}"
        gs3pk = f"BRAND#{brand_name}"
        gs3sk = f"CATEGORY#{category_name}"

        return cls(
            pk,
            sk,
            gs1pk,
            gs1sk,
            gs2pk,
            gs2sk,
            gs3pk,
            gs3sk,
            product_name,
            location_id,
            category_name,
            brand_name,
            description,
            price,
            total_stock_quantity,
            last_restock_date,
            inventory,
        )
