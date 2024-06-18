from typing import List
from uuid import UUID

from pydantic import BaseModel


class CreateBrand(BaseModel):
    name: str


class APIBrand(BaseModel):
    id: UUID
    name: str

    class ConfigDict:
        orm_mode = True


class APIBrandList(BaseModel):
    results: List[APIBrand]

    class ConfigDict:
        orm_mode = True
