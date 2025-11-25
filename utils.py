import pandas as pd
from .analyzer import analyze_sentiment

def analyze_csv(file, model="gpt-4.1-mini"):
    """
    Processes a CSV file containing a 'text' column and returns
    a DataFrame with: text | label | explanation | raw_response
    """

    df = pd.read_csv(file)

    if "text" not in df.columns:
        raise ValueError("CSV must include a column named 'text'.")

    results = []
    
    for text in df["text"].astype(str).fillna(""):
        result = analyze_sentiment(text, model=model)
        results.append({
            "text": text,
            "label": result["label"],
            "explanation": result["explanation"],
            "raw_response": result["raw_response"],
        })

    return pd.DataFrame(results)
