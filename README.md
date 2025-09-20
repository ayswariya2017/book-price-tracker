# Book Price Tracker

Small Python project that scrapes book data from BooksToScrape and tracks price changes.

## Features
- Scrapes Title, Price, Rating, Availability, and Product Link.
- Saves scraped data to CSV.
- Compares today's prices with previous run and reports price drops.
- Optional simple Streamlit UI to view results.

## How to run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the scraper:
   python scrape_books_full.py

3. Run the tracker (compares today's data with previous run):
   python price_tracker.py

4. (Optional) Run the UI:
   streamlit run app.py

## Notes
🔸 This project uses polite scraping: User-Agent header and time.sleep.

🔸 Only intended for educational purposes and allowed use on the demo website books.toscrape.com.