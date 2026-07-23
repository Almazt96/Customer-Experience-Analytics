# Interactive Streamlit Dashboard: a Streamlit interface allowing financial analysts to filter by bank, rating, and complaint theme
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ethiopian Fintech App Intelligence", layout="wide")

st.title("🏦 Ethiopian Mobile Banking Customer Intelligence")
st.markdown("Automated sentiment and customer experience analytics across CBE, BOA, and Dashen Bank.")

# Sidebar Filters
selected_bank = st.sidebar.multiselect("Select Banks", options=["CBE", "BOA", "Dashen"], default=["CBE", "BOA", "Dashen"])

# Dummy Data Loader (Replace with DB fetch query)
# df = fetch_data_from_db()

# Example KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews Analyzed", "1,450", "+12% this month")
col2.metric("Systemic Issue Alert", "OTP Failure", "High Frequency")
col3.metric("Avg Sentiment Score", "0.68 / 1.0", "Stable")

st.subheader("Sentiment Distribution Across Banks")
# Display Plotly Bar Chart / Heatmaps here