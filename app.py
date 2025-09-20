import streamlit as st
import pandas as pd
import subprocess
import os

st.title("Book Price Tracker")

if st.button("Scrape & Update Prices"):
    with st.spinner("Running scraper..."):
        subprocess.run(["python", "scrape_books_full.py"])
    st.success("Scraping finished. Saved to books_full.csv")

if os.path.exists("books_full.csv"):
    df = pd.read_csv("books_full.csv")
    st.write("Latest scraped data (first 50 rows):")
    st.dataframe(df.head(50))
else:
    st.info("No scraping result found. Click the button to scrape.")