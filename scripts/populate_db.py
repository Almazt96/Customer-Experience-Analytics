import os
import sys
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connection URL from environment variable or fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:leulalmaz@localhost:5432/bank_reviews")

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL: {e}")
        sys.exit(1)

def run_schema_migration(conn, schema_file_path="database/schema.sql"):
    """Executes the DDL statements from database/schema.sql."""
    if not os.path.exists(schema_file_path):
        logging.warning(f"Schema file {schema_file_path} not found. Skipping DDL execution.")
        return

    logging.info(f"Applying schema from {schema_file_path}...")
    with conn.cursor() as cur:
        with open(schema_file_path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
    conn.commit()
    logging.info("Schema applied successfully.")

def seed_banks(conn, bank_names):
    """Inserts distinct bank names and returns a dict mapping bank_name -> bank_id."""
    query = """
        INSERT INTO banks (bank_name)
        VALUES (%s)
        ON CONFLICT (bank_name) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.executemany(query, [(name,) for name in bank_names])
        conn.commit()

        cur.execute("SELECT bank_name, bank_id FROM banks;")
        bank_map = dict(cur.fetchall())
        
    logging.info(f"Seeded {len(bank_map)} bank entities into 'banks' table.")
    return bank_map

def batch_insert_reviews(conn, df, bank_map):
    """Performs efficient batch insertion of reviews using execute_values."""
    if df.empty:
        logging.warning("Provided DataFrame is empty. Skipping insertion.")
        return

    df["bank_id"] = df["bank_name"].map(bank_map)
    valid_reviews = df.dropna(subset=["bank_id"]).copy()

    records = []
    for _, row in valid_reviews.iterrows():
        records.append((
            int(row["bank_id"]),
            row.get("user_name", None),
            int(row["rating"]) if pd.notnull(row.get("rating")) else None,
            row.get("review_text", None),
            row.get("cleaned_text", None),
            row.get("sentiment_label", None),
            float(row["sentiment_score"]) if pd.notnull(row.get("sentiment_score")) else None,
            row.get("review_date", None)
        ))

    insert_query = """
        INSERT INTO reviews (
            bank_id, user_name, rating, review_text, 
            cleaned_text, sentiment_label, sentiment_score, review_date
        ) VALUES %s;
    """

    with conn.cursor() as cur:
        execute_values(cur, insert_query, records, page_size=1000)
        conn.commit()

    logging.info(f"Successfully inserted {len(records)} reviews into PostgreSQL!")

def populate_database(processed_csv_path="data/processed/cleaned_bank_reviews.csv"):
    conn = get_connection()
    try:
        # Step 1: Run DDL Schema Migration
        run_schema_migration(conn)

        # Step 2: Load processed CSV data
        if not os.path.exists(processed_csv_path):
            logging.error(f"Data file not found at {processed_csv_path}")
            return

        df = pd.read_csv(processed_csv_path)

        # Step 3: Standardize CSV headers to match expected pipeline names
        column_mapping = {
            'bank': 'bank_name',
            'userName': 'user_name',
            'score': 'rating',
            'content': 'review_text',
            'at': 'review_date'
        }
        df = df.rename(columns=column_mapping)

        if 'bank_name' not in df.columns:
            raise KeyError("DataFrame must contain 'bank_name' (or 'bank') column to map foreign keys.")

        # Step 4: Seed Banks and fetch FK mapping dict
        distinct_banks = df["bank_name"].dropna().unique().tolist()
        bank_map = seed_banks(conn, distinct_banks)

        # Step 5: Batch insert reviews
        batch_insert_reviews(conn, df, bank_map)

    finally:
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    populate_database()