# transform.py
import pandas as pd
from utils import (
    normalize_content_rating,
    normalize_country,
    normalize_duration,
    normalize_genre,
    normalize_rating,
    normalize_title,
    normalize_usd_numbers,
    normalize_votes,
    normalize_date,
)


def extract_and_clean_csv(file_path):
    df = pd.read_csv(file_path, sep=";", encoding="utf-8", on_bad_lines="skip")
    df = df.sort_values(by="IMBD title ID", ascending=True)

    df.columns = df.columns.str.strip()

    df["Original title"] = df["Original title"].apply(normalize_title)

    df = df.drop(columns=["Unnamed: 8"], errors="ignore")
    df.replace("", pd.NA, inplace=True)
    df = df.dropna(how="all")

    df["Release year"] = df["Release year"].apply(normalize_date)
    df["Release year"] = pd.to_datetime(df["Release year"], errors="coerce")

    df["Genre"] = df["Genre"].apply(normalize_genre)

    df["Duration"] = df["Duration"].apply(normalize_duration)

    df["Country"] = df["Country"].apply(normalize_country)

    df["Content Rating"] = df["Content Rating"].apply(normalize_content_rating)

    df = df.rename(columns={"Income": "Income_USD"})
    df["Income_USD"] = df["Income_USD"].apply(normalize_usd_numbers)

    df["Votes"] = df["Votes"].apply(normalize_votes)

    df["Score"] = df["Score"].apply(normalize_rating)

    return df


if __name__ == "__main__":
    df_clean = extract_and_clean_csv("messy_IMDB_dataset.csv")
    df_clean.to_csv("cleaned_IMDB_dataset.csv", index=False)
    print("Dataset cleaned !")
