import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE = "https://books.toscrape.com/"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

def parse_rating(css_class):
    # Site uses words like "One", "Two", ... mapped to ratings
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for cls in css_class:
        if cls in mapping:
            return mapping[cls]
    return None

with open("books_full.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Rating", "Availability", "ProductLink"])

    # There are 50 pages on this site
    for page in range(1, 51):
        page_url = urljoin(BASE, f"catalogue/page-{page}.html")
        res = requests.get(page_url, headers=headers)
        if res.status_code != 200:
            print(f"Stopped: page {page} returned {res.status_code}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            # Title
            title = book.h3.a["title"].strip()

            # Price (e.g. "£51.77"), strip currency sign
            price_text = book.find("p", class_="price_color").text.strip()
            price = price_text.replace("£", "").replace("Â", "").strip()

            # Rating (class contains word like "star-rating Three")
            rating = parse_rating(book.p["class"])

            # Availability (text inside <p class="instock availability">)
            availability = book.find("p", class_="instock availability").get_text().strip()

            # Link to product page (relative href)
            rel_link = book.h3.a["href"]
            product_link = urljoin(page_url, rel_link)  # build absolute URL

            writer.writerow([title, price, rating, availability, product_link])

        print(f"Page {page} scraped.")
        time.sleep(1.0)  # sleep 1 second between pages (politeness)
print("All done. Data saved to books_full.csv")