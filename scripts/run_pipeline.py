import os
import sys

# Calculate the path to the project root (one level up from 'scripts')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now your original import will work perfectly
from src.Task2thematicmapping import extract_banking_themes

import pandas as pd
from src.Task2thematicmapping import extract_banking_themes
from transformers import pipeline

def run_sentiment_and_thematic_pipeline(input_path: str, output_path: str):
    """
    Runs the entire Task 2 pipeline over the full dataset and saves the artifact.
    """
    # Load normalized data from Task 1
    df = pd.read_csv(input_path)
    print("Columns found in CSV:", df.columns.tolist())
    
    print("Step 1: Extracting Bank-Relevant Themes...")
    df = extract_banking_themes(df, text_column='content')
    
    print("Step 2: Running Full Sentiment Pipeline (DistilBERT)...")
    # Initialize your chosen transformer pipeline
    sentiment_analyzer = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english", 
        device=-1 # Set to 0 if running on GPU
    )
    
    labels = []
    scores = []
    
    # Process text column
    # (For massive datasets, wrap this in a batch processor or Dataset object)
    for text in df['content'].fillna(''):
        # Truncate text to fit model max length limits safely (512 tokens)
        truncated_text = text[:512] 
        result = sentiment_analyzer(truncated_text)[0]
        
        # Standardize naming strictly to rubric requirements
        labels.append(result['label'])
        scores.append(result['score'])
        
    df['sentiment_label'] = labels
    df['sentiment_score'] = scores
    
    # Step 3: Persist the final production artifact
    df.to_csv(output_path, index=False)
    print(f"Success! Production artifact successfully saved to: {output_path}")

if __name__ == "__main__":
    # Example execution targets
    run_sentiment_and_thematic_pipeline(
        input_path='./data/processed/cleaned_bank_reviews.csv',
        output_path='./data/processed/reviews_with_sentiment.csv'
    )

import logging

# Set up structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_task_2_pipeline(data):
    logger.info("Starting Task 2 Sentiment and Thematic Analysis pipeline.")
    
    if data.empty:
        logger.warning("Input DataFrame is empty. Proceeding with caution.")
        
    try:
        # Your analysis code here
        logger.info("Successfully completed theme mapping and sentiment scoring.")
    except Exception as e:
        logger.error(f"Pipeline failed during thematic analysis: {str(e)}")
        raise