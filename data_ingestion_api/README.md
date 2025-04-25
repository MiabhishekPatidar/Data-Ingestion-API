# Data Ingestion API

## Overview

This is a Flask-based API for uploading, storing, querying, and retrieving CSV data. The API allows users to upload CSV files, fetch stored data, query data dynamically, retrieve statistical summaries, and authenticate using JWT.

## Features

- **Upload CSV Files:** Store CSV data dynamically in an SQLite database.
- **Fetch Data:** Retrieve all stored data.
- **Query Data:** Dynamically filter data by any column.
- **Statistics:** Get insights like row count, column count, missing values, and numerical summaries.
- **Authentication:** Secure API endpoints using JWT authentication.

## Project Structure

```
project_root/
│── routes/
│   ├── get_data.py       # Fetch all stored data
│   ├── query_data.py     # Query stored data dynamically
│   ├── stats.py         # Retrieve dataset statistics
│   ├── upload.py        # Upload and store CSV data
│── venv/                # Virtual environment (dependencies)
│── app.py               # Main application entry point
│── auth.py              # Authentication (JWT)
│── config.py            # Configuration settings (API Key, JWT Secret)
│── data.db              # SQLite database
│── db.py                # Database helper functions
│── README.md            # Documentation
│── requirements.txt     # Required dependencies
```

## Installation

### Prerequisites

Ensure you have **Python 3.x** installed. Then, create a virtual environment and install dependencies.

```sh
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```sh
# Start the Flask application
python app.py
```

The API will run at: `http://127.0.0.1:5000/`

## API Endpoints

### 1. Authentication

#### **Login** (Generate JWT Token)

- **Endpoint:** `POST /login`
- **Request:**
  ```json
  { "api_key": "mysecureapikey" }
  ```
- **Response:**
  ```json
  { "access_token": "your_generated_jwt" }
  ```

### 2. Upload CSV Data

- **Endpoint:** `POST /upload`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Request:** Form-data with a CSV file (`file` key)
- **Response:**
  ```json
  { "message": "Data uploaded successfully" }
  ```

### 3. Fetch All Data

- **Endpoint:** `GET /get_data`
- **Response:**
  ```json
  {"data": [...], "status": "success"}
  ```

### 4. Query Data (Filter by Column)

- **Endpoint:** `GET /query_data`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Example:** `http://127.0.0.1:5000/query_data?name=Alice`
- **Response:**
  ```json
  {"data": [...], "status": "success"}
  ```

### 5. Get Data Statistics

- **Endpoint:** `GET /stats`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:**
  ```json
  {"status": "success", "statistics": {...}}
  ```

## Database Schema

- **uploaded_data** (Created dynamically based on uploaded CSV file)
- **csv_metadata** (Stores metadata about uploaded files)

## Notes

- Ensure that the database (`data.db`) is correctly initialized.
- Use JWT authentication for secured endpoints.
- The `/query_data` endpoint dynamically handles any CSV structure.

## License

MIT License
