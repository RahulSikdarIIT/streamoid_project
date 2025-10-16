import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import api, fetch_db_session
from database import OrmBase

TEST_SQLITE_URL = "sqlite:///./test_catalog.db"

test_engine = create_engine(
    TEST_SQLITE_URL, connect_args={"check_same_thread": False}
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

OrmBase.metadata.create_all(bind=test_engine)

def override_fetch_db_session():
    try:
        session = TestSession()
        yield session
    finally:
        session.close()

api.dependency_overrides[fetch_db_session] = override_fetch_db_session

api_client = TestClient(api)

@pytest.fixture(autouse=True)
def setup_test_database():
    OrmBase.metadata.drop_all(bind=test_engine)
    OrmBase.metadata.create_all(bind=test_engine)
    yield

def test_file_processing_logic():
    mock_csv_data = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "VALID-001,Valid Tee,GoodBrand,Red,M,1000,800,10\n"
        "VALID-002,Valid Jean,GoodBrand,Blue,32,2000,1500,5\n"
        "INVALID-MRP,Bad MRP,BadBrand,Red,M,1000,1200,10\n"
        "INVALID-QTY,Bad Qty,BadBrand,Red,M,1000,800,-5\n"
        "INVALID-REQ,Missing Price,BadBrand,Red,M,1000,,10\n"
    )
    upload_file_payload = {'product_file': ('test_products.csv', mock_csv_data, 'text/csv')}

    response = api_client.post("/upload", files=upload_file_payload)
    
    assert response.status_code == 200
    result_json = response.json()
    assert result_json["accepted"] == 2
    assert len(result_json["rejected"]) == 3
    assert result_json["rejected"][0]["reason"] == "Sale price exceeds MRP"
    assert result_json["rejected"][1]["reason"] == "Stock quantity cannot be negative"
    assert result_json["rejected"][2]["reason"] == "A required field is missing"

def test_item_search_filters():
    mock_csv_data_for_search = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "SHIRT-RED-01,Red Shirt,CoolThreads,Red,M,1200,900,10\n"
        "SHIRT-BLU-02,Blue Shirt,CoolThreads,Blue,L,1200,950,8\n"
        "JEANS-BLK-03,Black Jeans,DenimCo,Black,34,3000,2500,12\n"
    )
    upload_file_payload = {'product_file': ('test_data.csv', mock_csv_data_for_search, 'text/csv')}
    api_client.post("/upload", files=upload_file_payload)

    response = api_client.get("/products/search?brand_filter=CoolThreads")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = api_client.get("/products/search?min_price_filter=1000&max_price_filter=3000")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["sku"] == "JEANS-BLK-03"

    response = api_client.get("/products/search?brand_filter=NonExistentBrand")
    assert response.status_code == 200
    assert len(response.json()) == 0