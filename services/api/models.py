from dataclasses import dataclass
from enum import Enum
from uuid import UUID


@dataclass
class Brand:
    id: UUID
    name: str

    @classmethod
    def create(cls, id_, name):
        return cls(id_, name)
