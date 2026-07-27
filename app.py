import os
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from src.explainability import generate_text_shap_explanation

# Page Configuration
st.set_page_config(
    page_title="Ethiopian Fintech App Intelligence", layout="wide"
)

st.title("🏦 Ethiopian Mobile Banking Customer Intelligence")
st.markdown(
    "Automated sentiment and customer experience analytics across CBE, BOA, and Dashen Bank."
)


# -----------------------------------------------------------------------------
# 1. Resource & Model Loading (With Streamlit Caching)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_ml_assets():
    """Loads saved sentiment classifier and vectorizer from models/ directory."""
    model_path = "models/sentiment_classifier.joblib"
    vectorizer_path = "models/tfidf_vectorizer.joblib"

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None, None

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer


# Initialize model and vectorizer
model, vectorizer = load_ml_assets()

# -----------------------------------------------------------------------------
# 2. Sidebar Filters & Data Overview
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Options")
selected_bank = st.sidebar.multiselect(
    "Select Banks",
    options=["CBE", "BOA", "Dashen"],
    default=["CBE", "BOA", "Dashen"],
)

# Example KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews Analyzed", "1,450", "+12% this month")
col2.metric("Systemic Issue Alert", "OTP Failure", "High Frequency")
col3.metric("Avg Sentiment Score", "0.68 / 1.0", "Stable")

st.divider()

# -----------------------------------------------------------------------------
# 3. Analytics & Charts
# -----------------------------------------------------------------------------
st.subheader("Sentiment Distribution Across Banks")

# Sample chart data (Replace with database connection query)
sample_data = pd.DataFrame(
    {
        "Bank": ["CBE", "CBE", "BOA", "BOA", "Dashen", "Dashen"],
        "Sentiment": [
            "Positive",
            "Negative",
            "Positive",
            "Negative",
            "Positive",
            "Negative",
        ],
        "Count": [450, 200, 310, 180, 220, 90],
    }
)

filtered_df = sample_data[sample_data["Bank"].isin(selected_bank)]
fig = px.bar(
    filtered_df,
    x="Bank",
    y="Count",
    color="Sentiment",
    barmode="group",
    color_discrete_map={"Positive": "#2ecc71", "Negative": "#e74c3c"},
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 4. Model Explainability Section (SHAP)
# -----------------------------------------------------------------------------
st.subheader("🔍 Model Explainability & Local Interpretation")
st.markdown("Analyze feature importance for customer feedback reviews.")

review = st.text_area(
    "Enter a review text to evaluate:",
    value="The app keeps freezing during transfer and OTP is delayed",
)

if st.button("Explain Prediction with SHAP"):
    if model is None or vectorizer is None:
        st.error(
            "⚠️ Model or Vectorizer file not found! Please ensure 'sentiment_classifier.joblib' "
            "and 'tfidf_vectorizer.joblib' exist in the 'models/' directory."
        )
    else:
        with st.spinner("Generating SHAP feature breakdown..."):
            img_path = generate_text_shap_explanation(
                model=model, vectorizer=vectorizer, sample_text=review
            )

            st.image(
                img_path,
                caption="SHAP Local Feature Importance Breakdown",
                use_column_width=True,
            )