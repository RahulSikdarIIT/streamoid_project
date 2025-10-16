import io, pandas as pd
from fastapi import FastAPI,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from typing import List,Optional
import data_models,api_schemas
from database import db_connect_engine,AppSession,OrmBase

# --- init db + api ---
OrmBase.metadata.create_all(bind=db_connect_engine)
api = FastAPI(title="Product Catalog Service")

def fetch_db_session():
    """DB session per request (make sure it's closed properly)"""
    s = AppSession()
    try:
        yield s
    finally:
        s.close()


@api.get("/")
def show_welcome():
    return {"message": "Welcome!!"}

@api.post("/upload", tags=["Products"])
async def process_product_file(
    product_file: UploadFile = File(...),
    session: Session = Depends(fetch_db_session)
):
    try:
        # read CSV
        raw = await product_file.read()
        df = pd.read_csv(io.StringIO(raw.decode('utf-8')))
        df = df.where(pd.notnull(df), None)
    except Exception as e:
        # something went wrong with file format
        raise HTTPException(status_code=400, detail=f"Failed to parse provided csv file: {e}")
    saved = 0
    rejected = []
    mandatory = ['sku','name','brand','mrp','price']
    # print(df.head())  

    for i, row in df.iterrows():
        item = row.to_dict()
        if any(pd.isna(item.get(col)) for col in mandatory):
            rejected.append({"row":i+2, "reason":"missing required field"})
            continue
        if item['price'] > item['mrp']:
            rejected.append({"row":i+2, "reason":"price>MRP"})
            continue
        qty = item.get('quantity')
        if qty is not None and qty < 0:
            rejected.append({"row":i+2, "reason":"negative stock"})
            continue
        existing = session.query(data_models.Product).filter(
            data_models.Product.sku == item['sku']
        ).first()
        if not existing:
            new_entry = data_models.Product(**item)
            session.add(new_entry)
            saved+=1

    session.commit()
    return {"accepted": saved, "rejected": rejected}

@api.get("/products", response_model=List[api_schemas.ProductData], tags=["Products"])
def list_all_items(
    page_num: int = 1,
    page_size: int = 10,
    session: Session = Depends(fetch_db_session)
):
    if page_num<1:page_num=1
    if page_size<1:page_size=1
    skip = (page_num-1)*page_size
    data = session.query(data_models.Product).offset(skip).limit(page_size).all()
    return data


@api.get("/products/search", response_model=List[api_schemas.ProductData], tags=["Products"])
def find_products_by_filter(
    session: Session = Depends(fetch_db_session),
    brand_filter: Optional[str] = None,
    color_filter: Optional[str] = None,
    min_price_filter: Optional[float] = None,
    max_price_filter: Optional[float] = None
):
    q = session.query(data_models.Product)
    if brand_filter:
        q = q.filter(data_models.Product.brand.ilike(f"%{brand_filter}%"))
    if color_filter:
        q = q.filter(data_models.Product.color.ilike(f"%{color_filter}%"))
    if min_price_filter is not None:
        q = q.filter(data_models.Product.price>=min_price_filter)
    if max_price_filter is not None:
        q = q.filter(data_models.Product.price<=max_price_filter)
    result = q.all()
    # print(len(result))  
    return result



#by rahul -- rev1