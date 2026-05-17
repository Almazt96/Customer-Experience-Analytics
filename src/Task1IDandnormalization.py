import hashlib
import pandas as pd

def preprocess_review_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the review dataset by generating unique IDs, removing duplicates,
    and normalizing dates to YYYY-MM-DD.
    """
    # Create a copy to avoid SettingWithCopyWarning
    processed_df = df.copy()
    
    # 1. Generate a robust unique ID if it doesn't exist
    if 'review_id' not in processed_df.columns:
        # Create a deterministic hash based on username and raw date/text
        processed_df['review_id'] = processed_df.apply(
            lambda row: hashlib.md5(
                f"{row.get('username', '')}_{row.get('date', '')}".encode('utf-8')
            ).hexdigest(), 
            axis=1
        )
    
    # 2. Robust ID-based deduplication
    initial_count = len(processed_df)
    processed_df.drop_duplicates(subset=['review_id'], keep='first', inplace=True)
    print(f"Removed {initial_count - len(processed_df)} duplicate reviews.")
    
    # 3. Explicit Date Normalization (YYYY-MM-DD)
    # errors='coerce' turns unparseable dates into NaT, which we can then drop or flag
    processed_df['review_date'] = pd.to_datetime(processed_df['date'], errors='coerce')
    processed_df = processed_df.dropna(subset=['review_date']) # Clean out broken dates
    processed_df['review_date'] = processed_df['review_date'].dt.strftime('%Y-%m-%d')
    
    # 4. Handle Missing Ratings (Example: Imputing or dropping based on strict rules)
    # Assuming missing ratings should be flagged or dropped; here we drop them
    processed_df = processed_df.dropna(subset=['rating'])
    
    return processed_df