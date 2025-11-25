import sys
import os
import streamlit as st
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from src.utils import analyze_csv
from src.analyzer import analyze_sentiment

st.set_page_config(page_title="Sentiment Analyzer", page_icon="🧠", layout="wide")

st.title("🧠 Sentiment Analysis with OpenAI")
st.write("Upload a CSV file or enter text to analyze. Compatible with any OpenAI model.")

model = st.selectbox(
    "Select model:",
    ["gpt-4.1-mini", "gpt-4.1", "gpt-4.1-preview", "o3-mini"],
)

mode = st.radio("Analysis mode:", ["Single Text", "CSV File"])

# --- SINGLE TEXT ---
if mode == "Single Text":
    text = st.text_area("Enter your text:")

    if st.button("Analyze"):
        if not text.strip():
            st.error("Please enter some text before analyzing.")
        else:
            result = analyze_sentiment(text, model=model)

            st.subheader("Result")
            st.write("**Label:**", result["label"])
            st.write("**Explanation:**", result["explanation"])

            st.write("**Raw Model Response:**")
            st.code(result["raw_response"])

# --- CSV MODE ---
else:
    file = st.file_uploader("Upload a CSV file with a 'text' column", type=["csv"])

    if file and st.button("Process CSV"):
        df = analyze_csv(file, model=model)

        st.subheader("Analysis Results")
        st.dataframe(df, use_container_width=True)

        st.write("### 📊 Sentiment Summary")
        counts = df["label"].value_counts()

        col1, col2, col3 = st.columns(3)
        col1.metric("Positive", counts.get("positive", 0))
        col2.metric("Negative", counts.get("negative", 0))
        col3.metric("Neutral", counts.get("neutral", 0))

        st.write("### 📈 Distribution")
        st.bar_chart(counts)

        st.download_button(
            "Download results",
            data=df.to_csv(index=False),
            file_name="sentiment_results.csv",
            mime="text/csv",
        )
