from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeResponse(BaseModel):
    total_products: int
    products: List[Product]
