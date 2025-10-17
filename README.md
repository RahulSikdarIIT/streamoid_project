# Product Catalog API

A simple backend service for managing product catalogs from a CSV file.

## Core Features

* Upload a product catalog via a CSV file.
* Validate data for required fields and logical consistency.
* Store valid products in a SQLite database.
* List all products with pagination.
* Search for products by brand, color, or price range.

## Tech Stack

* **Backend:** Python, FastAPI
* **Database:** SQLite, SQLAlchemy
* **Testing:** Pytest
* **Deployment:** Docker

## How to Run

### Using Docker (Recommended)

Make sure you have Docker Desktop running.

1.  **Build the image:**
    ```bash
    docker build -t product-api .
    ```

2.  **Run the container in the background:**
    ```bash
    docker run -d -p 8000:8000 product-api
    ```
The API will be available at `http://localhost:8000`.

### Local Development

1.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server:**
    ```bash
    uvicorn main:api --reload
    ```

## How to Test

To run the unit tests, activate the virtual environment and run `pytest` from the project root.

```bash
pytest
```

## API Endpoints

Here’s a guide to using the API endpoints.

### 1. Upload CSV

Uploads and processes the product CSV file.

* **Endpoint:** `POST /upload`
* **Request (`curl`):**
    ```bash
    curl -X POST -F "product_file=@products.csv" http://localhost:8000/upload
    ```
* **Success Response:** (Using the provided example data)
    ```json
    {
      "accepted": 20,
      "rejected": []
    }
    ```

### 2. List Products

Fetches a paginated list of products.

* **Endpoint:** `GET /products`
* **Parameters:** `page_num` (int), `page_size` (int)
* **Request (`curl`):** (Gets the first page with 2 items)
    ```bash
    curl "http://localhost:8000/products?page_num=1&page_size=2"
    ```
* **Success Response:**
    ```json
    [
      {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "Stream Threads",
        "color": "Red",
        "size": "M",
        "mrp": 799.0,
        "price": 499.0,
        "quantity": 20
      },
      {
        "sku": "TSHIRT-BLK-002",
        "name": "Classic Cotton T-Shirt",
        "brand": "Stream Threads",
        "color": "Black",
        "size": "L",
        "mrp": 799.0,
        "price": 549.0,
        "quantity": 12
      }
    ]
    ```

### 3. Search Products

Searches products based on filters.

* **Endpoint:** `GET /products/search`
* **Parameters:** `brand_filter` (str), `color_filter` (str), `min_price_filter` (float), `max_price_filter` (float)
* **Request (`curl`):** (Finds products from BloomWear under 2500)
    ```bash
    curl "http://localhost:8000/products/search?brand_filter=BloomWear&max_price_filter=2500"
    ```
* **Success Response:**
    ```json
    [
      {
        "sku": "DRESS-PNK-S",
        "name": "Floral Summer Dress",
        "brand": "BloomWear",
        "color": "Pink",
        "size": "S",
        "mrp": 2499.0,
        "price": 2199.0,
        "quantity": 10
      },
      {
        "sku": "DRESS-YLW-M",
        "name": "Floral Summer Dress",
        "brand": "BloomWear",
        "color": "Yellow",
        "size": "M",
        "mrp": 2499.0,
        "price": 1999.0,
        "quantity": 7
      }
    ]
    ```