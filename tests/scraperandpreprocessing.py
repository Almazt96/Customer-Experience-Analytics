# scraperandpreprocessing.py
import pandas as pd
from google_play_scraper import Sort, reviews
import psycopg2
from sqlalchemy import create_engine

print("Libraries loaded successfully.")

# --- Database Connection Logic Wrapper ---
def get_db_engine():
    """Creates database engine securely when called."""
    try:
        # Replace with your actual database details if necessary
        engine = create_engine('postgresql://postgres:leulalmaz@localhost:5432/mobileapp')
        print("🎉 Connected successfully to the mobileapp database!")
        return engine
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# --- Main Scraping Function ---
def scrape_bank_reviews(app_id, bank_name):
    try:
        result, _ = reviews(
            app_id,
            lang='en', 
            country='et', 
            sort=Sort.NEWEST, 
            count=500 
        )
        df = pd.DataFrame(result)
        if not df.empty:
            df['bank'] = bank_name
        return df
    except Exception as e:
        print(f"Error scraping {bank_name}: {e}")
        return pd.DataFrame() # Return empty dataframe on failure

# --- Controlled Execution Block ---
# Everything below ONLY runs when executing this file directly.
# When running tests, this entire block is ignored by Python.
if __name__ == "__main__":
    
    # 1. Connect to database
    engine = get_db_engine()
    
    # 2. Define targets
    apps_to_scrape = {
        'CBE': 'com.combanketh.mobilebanking',
        'BOA': 'com.boa.boaMobileBanking',
        'Dashen': 'com.dashen.dashensuperapp'
    }
    
    scraped_dfs = []
    
    # 3. Process each app
    for bank_name, app_id in apps_to_scrape.items():
        print(f"Scraping {bank_name} using ID: {app_id}...")
        df_bank = scrape_bank_reviews(app_id, bank_name)
        
        print(f"Found {len(df_bank)} reviews for {bank_name}.")
        if not df_bank.empty:
            scraped_dfs.append(df_bank)
        else:
            print(f"⚠️ Warning: No data returned for {bank_name}. Check the App ID or country code.")

    # 4. Save and export safely inside the main block
    if scraped_dfs:
        all_reviews = pd.concat(scraped_dfs, ignore_index=True)
        all_reviews.to_csv('./data/raw/bank_reviews.csv', index=False)
        print("\n✅ Success! Scraping completed and saved to bank_reviews.csv")
        print(f"Total reviews collected: {len(all_reviews)}")
        print(all_reviews['bank'].value_counts())
        
        # Optional: Save to your database if engine is alive
        if engine:
            try:
                all_reviews.to_sql('bank_reviews', engine, if_exists='append', index=False)
                print("💾 Data successfully mirrored to PostgreSQL database.")
            except Exception as e:
                print(f"❌ Failed to save data to database: {e}")
    else:
        print("\n❌ Error: No reviews were collected for any bank. CSV not updated.")
        
    """ Preprocessing and Cleaning Steps
After scraping, we need to clean the data to ensure we have 400 clean reviews for each bank. This involves:
1. Removing any duplicate reviews
2. Filtering out reviews that are too short or contain inappropriate content
3. Standardizing the format of the reviews
4. Handling missing values appropriately """
# Example of cleaning the data
def clean_reviews(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=['content'])
    
    # Filter out short reviews (e.g., less than 10 characters)
    df = df[df['content'].str.len() >= 10]
    
    # Optionally, filter out reviews with inappropriate content using a simple keyword filter
    inappropriate_keywords = ['bad', 'worst', 'terrible']  # Example keywords
    df = df[~df['content'].str.contains('|'.join(inappropriate_keywords), case=False)]
    
    # Handle missing values (e.g., fill with 'No review' or drop)
    df['content'] = df['content'].fillna('No review')
    
    return df
# Apply cleaning to each bank's reviews
if scraped_dfs:
    cleaned_dfs = [clean_reviews(df) for df in scraped_dfs]
    all_cleaned_reviews = pd.concat(cleaned_dfs, ignore_index=True)
    all_cleaned_reviews.to_csv('./data/cleaned/cleaned_bank_reviews.csv', index=False)
    print("\n✅ Cleaning completed and saved to cleaned_bank_reviews.csv")
    print(f"Total clean reviews collected: {len(all_cleaned_reviews)}")
    print(all_cleaned_reviews['bank'].value_counts()) # Shows breakdown per bank
else:
    print("\n❌ Error: No reviews to clean. CSV not updated.")
    