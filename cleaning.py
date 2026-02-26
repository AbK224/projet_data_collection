import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df["prix"] = df["prix"].astype(str).str.replace("CFA", "").str.replace(" ", "")
    df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    return df