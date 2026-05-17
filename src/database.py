import os
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import psycopg2

print("Libraries and DLLs loaded successfully.")

# 1. Define your credentials
user = "postgres" 
password_raw = "leulalmaz"  # Contains '@', must be URL-encoded
host = "localhost"
port = "5432"
dbname = "mobileapp"

""" # 2. URL-encode the password to handle the '@' character safely
safe_password = urllib.parse.quote_plus(password_raw) """

# 3. Construct the connection string
conn_string = f"postgresql://{user}:{password_raw}@{host}:{port}/{dbname}"
print(f"Constructed connection string: {conn_string}")

# 4. Create a single, reusable engine
engine = create_engine(conn_string)

# 5. Test the connection
try:
    with engine.connect() as conn:
        print("🎉 Successfully connected to PostgreSQL!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1) # Stop script execution if connection fails

# 6. Load data from CSV file and write to SQL
csv_file_path = './data/processed/cleaned_bank_reviews.csv' # Update this path if your file is located elsewhere

if os.path.exists(csv_file_path):
    print(f"Reading data from {csv_file_path}...")
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(f"Loaded {len(df)} rows from CSV. Appending to database table 'cleaned_reviews'...")
    
    try:
        # Write to SQL table named 'cleaned_reviews'
        # if_exists='append' adds data to the table without deleting existing entries
        df.to_sql('cleaned_reviews', engine, if_exists='append', index=False)
        print("✅ Dataframe written to database successfully!")
        
    except Exception as e:
        print(f"❌ Failed to write dataframe to database: {e}")
else:
    print(f"⚠️ Warning: Target CSV file not found at '{csv_file_path}'. Data loading skipped.")