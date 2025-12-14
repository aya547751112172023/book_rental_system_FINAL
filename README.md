<<<<<<< HEAD
<<<<<<< HEAD
# FastAPI + MySQL Project Starter

A robust project template for building REST APIs with **FastAPI** and **`mysql-connector-python`**. This project provides a clean structure for handling database operations, data validation, and API routing.

---

## ✨ Features

- **FastAPI:** Modern, high-performance web framework for building APIs.
- **MySQL:** Uses `mysql-connector-python` with connection pooling for efficient database management.
- **Pydantic:** Used for data validation (in `models.py`).
- **Dependency Injection:** Uses FastAPI's `Depends` system to manage database connections.
- **Auto-generated Docs:** Provides interactive API documentation (Swagger UI & ReDoc).

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.8+**
- **A running MySQL (or MariaDB) server**

### 2. Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/kayljiyan/fastapi-mysql
    cd fastapi-mysql
    ```

2.  **Create and activate a virtual environment:**

    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Database Setup

1.  **Log in to your MySQL server:**

    ```bash
    mysql -u your_username -p
    ```

2.  **Create your database:**

    ```sql
    CREATE DATABASE your_database_name;
    ```

3.  **Create your tables:**
    Run the SQL script (e.g., `setup.sql` or similar) that contains your `CREATE TABLE` statements.

### 4. Environment Configuration

This project loads database credentials from a `.env` file.

1.  **Create a file named `.env`** in the root of the project.
2.  **Add your database credentials:**

    ```ini
    # .env
    DB_HOST=localhost
    DB_USER=your_mysql_username
    DB_PASSWORD=your_mysql_password
    DB_NAME=your_database_name
    ```

    > **Note:** This `.env` file is listed in `.gitignore` and should never be committed to your repository.

---

## 🏃‍♂️ Running the Server

With your virtual environment active and the `.env` file in place, run the server using Uvicorn:

```bash
uvicorn main:app --reload
```
=======
# book_rental_system_F
 00f4885bdb0da0b0a293b0ca358e698361e4fbef
=======
# book_rental_system_FINAL
 8a93245755b9a3b2db8805761868ab567e252988
