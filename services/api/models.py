from dataclasses import dataclass
from uuid import UUID


@dataclass
class Brand:
    id: UUID
    name: str

    @classmethod
    def create(cls, id_, name):
        return cls(id_, name)
