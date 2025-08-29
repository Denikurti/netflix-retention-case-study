"""
Netflix Retention Case Study
Author: Deni Kurti

Goal: Understand cohort retention, content mix trends, and country differences, then outline actions to improve retention.

Business Questions:
1) How does retention change by customers’ first-watch month (cohorts)?
2) Which genres have grown or declined over time?
3) Which countries contribute the most titles and how is the mix different?
4) (Optional) Can a simple baseline model flag likely churners?

Dataset: data/raw/netflix_titles.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load data
raw_path = "data/raw/netflix_titles.csv"  # TODO: put dataset here
df = pd.read_csv(raw_path)

print("✅ Data loaded. Shape:", df.shape)
print(df.head())

# --- Step 3A: Cleaning + quick schema ---
# 1) Standardize column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# 2) Drop duplicates just in case
before = len(df)
df = df.drop_duplicates()
after = len(df)

# 3) Parse dates
if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["added_year"] = df["date_added"].dt.year
    df["added_month"] = df["date_added"].dt.to_period("M").dt.to_timestamp()

print("\n✅ Cleaning done.")
print(f"Duplicates removed: {before - after}")
print("📦 Columns:", list(df.columns))
print("\n🧹 Top null counts:")
print(df.isna().sum().sort_values(ascending=False).head(10))

if "rating" in df.columns:
    print("\n🔤 Rating distribution (top 10):")
    print(df["rating"].value_counts().head(10))

if "listed_in" in df.columns:
    print("\n🎭 Sample genres from 'listed_in':")
    print(df["listed_in"].dropna().head(3).to_list())

# --- Step 3B: Visualization — Titles added by year ---
import os
os.makedirs("figures", exist_ok=True)

if "added_year" in df.columns:
    year_counts = (
        df.dropna(subset=["added_year"])
          .groupby("added_year")["show_id"]
          .count()
          .sort_index()
    )

    print("\n📈 Titles added by year (head):")
    print(year_counts.head())

    plt.figure(figsize=(10, 5))
    year_counts.plot(kind="bar")
    plt.title("Titles Added by Year")
    plt.xlabel("Year Added to Netflix")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    out_path = "figures/titles_added_by_year.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved figure → {out_path}")
else:
    print("⚠️ 'added_year' not found — skip 3B.")

# --- Step 3C: Visualization — Top 15 Genres ---
import os
os.makedirs("figures", exist_ok=True)

if "listed_in" in df.columns:
    genres = (
        df.dropna(subset=["listed_in"])
          .assign(listed_in=df["listed_in"].str.split(","))
          .explode("listed_in")
    )
    genres["listed_in"] = genres["listed_in"].str.strip()

    top_genres = genres["listed_in"].value_counts().head(15).sort_values()

    print("\n🎭 Top genres (counts):")
    print(top_genres.sort_values(ascending=False))

    plt.figure(figsize=(10, 6))
    top_genres.plot(kind="barh")
    plt.title("Top 15 Genres on Netflix")
    plt.xlabel("Count of Titles")
    plt.ylabel("Genre")
    plt.tight_layout()
    out_path = "figures/top_15_genres.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved figure → {out_path}")
else:
    print("⚠️ 'listed_in' not found — skip 3C.")

# --- Step 3D: Visualization — Top 10 Countries ---
# --- Step 3D: Visualization — Top 10 Countries ---
os.makedirs("figures", exist_ok=True)

if "country" in df.columns:
    countries = (
        df.dropna(subset=["country"])
          .assign(country=df["country"].str.split(","))
          .explode("country")
    )
    countries["country"] = countries["country"].str.strip()

    top_countries = countries["country"].value_counts().head(10)

    print("\n🌍 Top 10 countries (counts):")
    print(top_countries)

    plt.figure(figsize=(10, 5))
    top_countries.plot(kind="bar")
    plt.title("Top 10 Countries by Number of Titles")
    plt.xlabel("Country")
    plt.ylabel("Count of Titles")
    plt.tight_layout()
    out_path = "figures/top_10_countries.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved figure → {out_path}")
else:
    print("⚠️ 'country' column not found — skip 3D.")

# --- Step 3E: Visualization — Genre trends over time (Top 6) ---
os.makedirs("figures", exist_ok=True)

if {"listed_in", "added_year"}.issubset(df.columns):
    # explode genres
    g = (
        df.dropna(subset=["listed_in", "added_year"])
          .assign(listed_in=df["listed_in"].str.split(","))
          .explode("listed_in")
    )
    g["listed_in"] = g["listed_in"].str.strip()
    # make year int
    g["added_year"] = g["added_year"].astype(int)

    # pick top 6 genres overall
    top6 = g["listed_in"].value_counts().head(6).index.tolist()

    genre_year = (
        g[g["listed_in"].isin(top6)]
        .groupby(["added_year", "listed_in"])
        .size()
        .reset_index(name="count")
        .sort_values(["added_year", "listed_in"])
    )

    print("\n🗓️ Genre trends sample:")
    print(genre_year.head(10))

    # pivot to year x genre matrix
    mat = genre_year.pivot(index="added_year", columns="listed_in", values="count").fillna(0)

    plt.figure(figsize=(10, 6))
    mat.plot(ax=plt.gca())
    plt.title("Top 6 Genres Added per Year")
    plt.xlabel("Year Added")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    out_path = "figures/genre_trends_top6_by_year.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Saved figure → {out_path}")
else:
    print("⚠️ Need 'listed_in' and 'added_year' to plot genre trends — skip 3E.")

# --- Step 3F: Save cleaned data + exports ---
import os
os.makedirs("data/processed", exist_ok=True)

clean_path = "data/processed/netflix_titles_clean.parquet"
df.to_parquet(clean_path, index=False)

# also export quick summaries you already computed
# (recompute small ones here to keep code self-contained)
top_genres_csv = "data/processed/top_genres.csv"
top_countries_csv = "data/processed/top_countries.csv"

# genres
g = (
    df.dropna(subset=["listed_in"])
      .assign(listed_in=df["listed_in"].str.split(","))
      .explode("listed_in")
)
g["listed_in"] = g["listed_in"].str.strip()
g["listed_in"].value_counts().to_csv(top_genres_csv, header=["count"])

# countries
c = (
    df.dropna(subset=["country"])
      .assign(country=df["country"].str.split(","))
      .explode("country")
)
c["country"] = c["country"].str.strip()
c["country"].value_counts().to_csv(top_countries_csv, header=["count"])

print(f"\n💾 Saved cleaned data → {clean_path}")
print(f"💾 Saved genre counts → {top_genres_csv}")
print(f"💾 Saved country counts → {top_countries_csv}")

