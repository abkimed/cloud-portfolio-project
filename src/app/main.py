import os

import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Portfolio Microservice", version="1.0.0")

# Database connection details passed from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


@app.get("/health", status_code=200)
def health_check():
    """Liveness probe for Load Balancer and ECS health checks."""
    return {"status": "healthy", "service": "cloud-portfolio-app"}


@app.get("/db-check")
def db_check():
    """Validates connectivity to the PostgreSQL RDS instance."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            connect_timeout=3,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "connected", "database_version": db_version[0]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e!s}")
