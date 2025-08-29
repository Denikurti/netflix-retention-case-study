# Netflix Retention Case Study
Goal: explore retention by cohort, content mix trends, country segmentation, and a simple churn baseline.

## Structure
- data/raw/        # original data
- data/processed/  # cleaned data
- notebooks/       # main analysis notebook
- figures/         # exported charts

## How to run
1) python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) jupyter notebook notebooks/netflix_retention.ipynb

4) ## Preview

![Titles Added by Year](figures/titles_added_by_year.png)

![Top 15 Genres](figures/top_15_genres.png)

![Top 10 Countries](figures/top_10_countries.png)

![Genre Trends Over Time (Top 6)](figures/genre_trends_top6_by_year.png)

