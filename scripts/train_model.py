import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Load dataset (update filename if your processed CSV has a different name)
data_path = "data/processed/cleaned_bank_reviews.csv"

if not os.path.exists(data_path):
    # Fallback check if the path is slightly different
    possible_paths = ["data/reviews.csv", "data/cleaned_reviews.csv", "data/fintech_reviews.csv"]
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break

print(f"Loading data from: {data_path}")
df = pd.read_csv(data_path)

print("\n--- Columns found in your dataset ---")
print(df.columns.tolist())
print("------------------------------------\n")

# 2. Auto-detect text and target column names
possible_text_cols = ['content', 'review', 'cleaned_text', 'review_text', 'text', 'translated_content']
possible_target_cols = ['sentiment', 'score', 'rating', 'label', 'target']

text_col = next((col for col in possible_text_cols if col in df.columns), None)
target_col = next((col for col in possible_target_cols if col in df.columns), None)

if not text_col or not target_col:
    print("ERROR: Could not automatically identify your columns.")
    print(f"Available columns are: {df.columns.tolist()}")
    print("Please set text_col and target_col manually near the top of train_model.py.")
    exit(1)

print(f"-> Selected Text Column: '{text_col}'")
print(f"-> Selected Target Column: '{target_col}'\n")

# Drop any rows with missing values in these columns
df = df.dropna(subset=[text_col, target_col])

X = df[text_col]
y = df[target_col]

# 3. Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y if len(y.unique()) > 1 else None
)

# 4. Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

# 5. Model Training
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# 6. Save both Model and Vectorizer
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/sentiment_classifier.joblib")
joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")

print("Success! Model and TF-IDF vectorizer saved to the 'models/' directory.")