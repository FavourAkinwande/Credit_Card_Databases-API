# Credit_Card_Databases-API

A FastAPI project for managing credit card transactions, features, models, and predictions using PostgreSQL and SQLAlchemy.

---

## Features

- RESTful CRUD API for users, transactions, transaction features, logs, ML models, and predictions
- PostgreSQL relational database with stored procedures and triggers
- SQLAlchemy ORM models
- Health check endpoint for database connectivity

---

## Prerequisites

- Python 3.8+
- Docker (for running PostgreSQL, optional but recommended)
- PostgreSQL database (local or Docker)
- pip (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Credit_Card_Databases-API
```

### 2. Set Up Python Environment

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env` template and fill in your PostgreSQL credentials:

```bash
cp .env .env.local
```

Edit `.env.local` (or `.env`) with your settings:

```
DATABASE_URL=postgresql+psycopg2://your_username:your_password@localhost:5432/your_database
```

Or use the provided variables to construct the URL.

### 5. Set Up the Database

- Start your PostgreSQL server (locally or via Docker).
- Create the database if it does not exist.
- Run the schema SQL to create tables, stored procedures, and triggers:

```bash
psql -U your_username -d your_database -f Credit_Card_Databases-API/schema.sql
```

### 6. Run the FastAPI Application

```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at [http://127.0.0.1:8080](http://127.0.0.1:8080).

---

## API Usage

### Health Check

Test the database connection:

```bash
curl http://127.0.0.1:8080/health/db
```

Expected response if the DB is connected:

```json
{"db_status": "ok"}
```

---

## Example .env File

```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg2://your_username:your_password@localhost:5432/your_database
```

---

## Project Structure

```
Credit_Card_Databases-API/
│
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # DB connection/session
│   └── ...              # (routers, schemas, etc.)
├── schema.sql           # PostgreSQL schema, procedures, triggers
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
└── README.md            # Project documentation
```

---

## License

MIT License (or specify your license here)