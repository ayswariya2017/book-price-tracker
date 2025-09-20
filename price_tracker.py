import os
import pandas as pd
import subprocess
import time
from datetime import datetime

# Step A: Run the previous scraper to produce books_today.csv
subprocess.run(["python", "scrape_books_full.py"], check=True)

today_file = "books_today.csv"
if os.path.exists("books_full.csv"):
    os.replace("books_full.csv", today_file)

# Step B: load today's data
df_today = pd.read_csv(today_file)
# ensure price is numeric
df_today["Price"] = (df_today["Price"].astype(str).str.replace("£", "", regex=False).str.replace("Â", "", regex=False).str.strip().astype(float))

# Step C: load previous data if exists
prev_file = "books_prev.csv"
if os.path.exists(prev_file):
    df_prev = pd.read_csv(prev_file)
    df_prev["Price"] = (df_prev["Price"].astype(str).str.replace("£", "", regex=False).str.replace("Â", "", regex=False).str.strip().astype(float))
else:
    df_prev = pd.DataFrame(columns=df_today.columns)

# Step D: compare by product link (unique id)
merged = pd.merge(df_prev, df_today, on="ProductLink", how="right", suffixes=("_prev", "_today"))

# Step E: find price drops
drops = merged[
    (merged["Price_prev"].notna()) & 
    (merged["Price_today"] < merged["Price_prev"])
]

if not drops.empty:
    print("Price drops found:")
    for _, row in drops.iterrows():
        print(f"- {row['Title_today']} : {row['Price_prev']} → {row['Price_today']} | {row['ProductLink']}")
else:
    print("No price drops found.")

# Step F: rotate files: today's becomes prev for next run
if os.path.exists(prev_file):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.replace(prev_file, f"books_prev_{timestamp}.csv")
os.replace(today_file, prev_file)

# Optional: send email alert (requires SMTP setup)
def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_pass):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)