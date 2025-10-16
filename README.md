# Product Catalog API

A robust backend service built with FastAPI to upload, validate, store, and query product catalog data from a CSV file. This project is designed to simulate a real-world scenario where online sellers need to manage their product data before listing it on marketplaces.

---

## ✨ Features

* [cite_start]**CSV Upload**: A dedicated endpoint to upload product data in CSV format[cite: 16].
* [cite_start]**Data Validation**: Each product row is validated against a set of business rules (e.g., price must be less than MRP, required fields must be present)[cite: 33, 34, 35, 36].
* [cite_start]**Database Storage**: Valid product data is stored securely in a SQLite database[cite: 37].
* [cite_start]**Paginated Listing**: An API to list all stored products with support for pagination to handle large datasets efficiently[cite: 40].
* [cite_start]**Dynamic Search**: A powerful search API to filter products by brand, color, and price range[cite: 43].
* [cite_start]**Dockerized**: The entire application is containerized with Docker for easy setup and consistent deployment in any environment[cite: 57].
* [cite_start]**Unit Tested**: Core functionalities like CSV parsing, validation, and search are covered by unit tests using `pytest`[cite: 57].

---

## 🛠️ Tech Stack

* **Language**: Python 3.11
* **Framework**: FastAPI
* **Database**: SQLite
* **Data Handling**: Pandas
* **Database ORM**: SQLAlchemy
* **Testing**: Pytest
* **Containerization**: Docker

---

## 🚀 Getting Started

There are two ways to get the application running: using Docker (recommended) or setting it up locally.

### Method 1: Running with Docker (Recommended)

This is the easiest and most reliable way to run the service.

**Prerequisites:**
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

**Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd product_catalog_api
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t product-api .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 product-api
    ```

The API will now be running and accessible at `http://localhost:8000`.

### Method 2: Local Setup (Without Docker)

**Prerequisites:**
* Python 3.9+ installed.

**Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd product_catalog_api
    ```

2.  **Create and activate a virtual environment:**
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:api --reload
    ```

The API will now be running and accessible at `http://localhost:8000`.

---

## 🧪 Running Tests

To ensure the reliability and correctness of the application logic, you can run the suite of unit tests.

1.  Make sure you have completed the **Local Setup** steps above.
2.  From the root directory of the project, run `pytest`:
    ```bash
    pytest
    ```
    The tests will run against a separate, temporary test database to avoid interfering with your main data.

---

## 📖 API Documentation

The API provides three main endpoints to manage the product catalog.

### 1. Upload Product CSV

Uploads a CSV file, validates each row, and stores valid products in the database.

* **URL**: `/upload`
* **Method**: `POST`
* **Content-Type**: `multipart/form-data`

**Sample Request (`curl`):**
```bash
curl -X POST -F "product_file=@products.csv" http://localhost:8000/upload
```

**Sample Success Response:**
```json
{
  "accepted": 18,
  "rejected": [
    {
      "row": 4,
      "reason": "Sale price exceeds MRP"
    }
  ]
}
```

### 2. List All Products

Retrieves a paginated list of all products stored in the database.

* **URL**: `/products`
* **Method**: `GET`
* **Query Parameters**:
    * `page_num` (optional, integer, default: `1`): The page number to retrieve.
    * `page_size` (optional, integer, default: `10`): The number of items per page.

**Sample Request (`curl`):**
```bash
curl "http://localhost:8000/products?page_num=1&page_size=2"
```

**Sample Success Response:**
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

Searches for products based on a combination of filters.

* **URL**: `/products/search`
* **Method**: `GET`
* **Query Parameters**:
    * `brand_filter` (optional, string): Filter by brand name (case-insensitive).
    * `color_filter` (optional, string): Filter by color (case-insensitive).
    * `min_price_filter` (optional, float): Filter for products with a price greater than or equal to this value.
    * `max_price_filter` (optional, float): Filter for products with a price less than or equal to this value.

**Sample Request (`curl`):**
```bash
curl "http://localhost:8000/products/search?brand_filter=BloomWear&max_price_filter=2500"
```

**Sample Success Response:**
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
  }
]
```