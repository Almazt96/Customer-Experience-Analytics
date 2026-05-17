import pandas as pd
from google_play_scraper import Sort, reviews
print("Library loaded successfully.")

def scrape_bank_reviews(app_id, bank_name):
    result, _ = reviews(
        app_id,
        lang='en', 
        country='et', 
        sort=Sort.NEWEST, 
        count=500 # Aim for 500 to ensure 400 clean ones
    )
    df = pd.DataFrame(result)
    df['bank'] = bank_name
    return df

if __name__ == "__main__":
    # Corrected Google Play App IDs
    # Note: If 'com.cbe.cbe_mobile' doesn't fetch enough, use 'com.cbe.cbebirr' depending on which app you want to target
    apps_to_scrape = {

        'CBE': 'com.combanketh.mobilebanking',
        'BOA': 'com.boa.boaMobileBanking',
        'Dashen': 'com.dashen.dashensuperapp'
    }
    
    scraped_dfs = []
    
    for bank_name, app_id in apps_to_scrape.items():
        print(f"Scraping {bank_name} using ID: {app_id}...")
        df_bank = scrape_bank_reviews(app_id, bank_name)
        
        print(f"Found {len(df_bank)} reviews for {bank_name}.")
        if not df_bank.empty:
            scraped_dfs.append(df_bank)
        else:
            print(f"⚠️ Warning: No data returned for {bank_name}. Check the App ID or country code.")

    # Only combine and save if we actually got data
    if scraped_dfs:
        all_reviews = pd.concat(scraped_dfs, ignore_index=True)
        all_reviews.to_csv('./data/raw/bank_reviews.csv', index=False)
        print("\n✅ Success! Scraping completed and saved to bank_reviews.csv")
        print(f"Total reviews collected: {len(all_reviews)}")
        print(all_reviews['bank'].value_counts()) # Shows breakdown per bank
    else:
        print("\n❌ Error: No reviews were collected for any bank. CSV not updated.")

    result, _ = reviews(
        app_id,
        lang='en', 
        country='et',  # Changed from 'us' to 'et' (Ethiopia)
        sort=Sort.NEWEST, 
        count=500
    )