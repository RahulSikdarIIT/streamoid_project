from pydantic import BaseModel,ConfigDict
from typing import Optional

class ProductData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sku: str
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: float
    price: float
    quantity: Optional[int] = None