from pydantic import BaseModel


class Item(BaseModel):
    state: str
    city: str
    port: str
    price: int
