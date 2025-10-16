from sqlalchemy import Column,Integer,String,Float
from database import OrmBase

class Product(OrmBase):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String)
    size = Column(String)
    mrp = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer)