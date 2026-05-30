import os
import time
import pandas as pd
import feedparser
from urllib.parse import quote

# =========================
# SETTING
# =========================
OUTPUT_PATH = "data/berita.csv"

START_YEAR = 2024
END_YEAR = 2026

SLEEP_TIME = 0

TICKERS_KEYWORDS = {
    "BBCA.JK": ["BBCA saham", "BCA saham", "Bank Central Asia"],
    "BBRI.JK": ["BBRI saham", "BRI saham", "Bank Rakyat Indonesia"],
    "BMRI.JK": ["BMRI saham", "Bank Mandiri saham"],
    "BBNI.JK": ["BBNI saham", "BNI saham"],
    "TLKM.JK": ["TLKM saham", "Telkom Indonesia saham"],
    "ASII.JK": ["ASII saham", "Astra International saham"],
    "UNVR.JK": ["UNVR saham", "Unilever Indonesia saham"],
    "ICBP.JK": ["ICBP saham", "Indofood CBP saham"],
    "INDF.JK": ["INDF saham", "Indofood saham"],
    "ANTM.JK": ["ANTM saham", "Aneka Tambang saham"],
    "ADRO.JK": ["ADRO saham", "Adaro Energy saham"],
    "PTBA.JK": ["PTBA saham", "Bukit Asam saham"],
    "GOTO.JK": ["GOTO saham", "GoTo saham"],
    "AMRT.JK": ["AMRT saham", "Alfamart saham"],
    "KLBF.JK": ["KLBF saham", "Kalbe Farma saham"],
}

# =========================
# RANGE PER KUARTAL
# =========================
def generate_quarter_ranges(start_year, end_year):
    ranges = []

    for year in range(start_year, end_year + 1):
        quarters = [
            (f"{year}-01-01", f"{year}-04-01"),
            (f"{year}-04-01", f"{year}-07-01"),
            (f"{year}-07-01", f"{year}-10-01"),
            (f"{year}-10-01", f"{year + 1}-01-01"),
        ]

        ranges.extend(quarters)

    return ranges

# =========================
# AMBIL GOOGLE NEWS RSS
# =========================
def fetch_google_news(keyword, ticker, start_date, end_date):

    query = f'{keyword} after:{start_date} before:{end_date}'

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}"
        "&hl=id"
        "&gl=ID"
        "&ceid=ID:id"
    )

    feed = feedparser.parse(url)

    rows = []

    for entry in feed.entries:

        published = getattr(entry, "published", None)
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")

        if published and title:

            date = pd.to_datetime(
                published,
                errors="coerce"
            )

            if pd.notna(date):

                rows.append({
                    "Date": date.date(),
                    "Ticker": ticker,
                    "News_Text": title,
                    "Keyword": keyword,
                    "Source": "Google News RSS",
                    "URL": link
                })

    return rows

# =========================
# SAVE DATA
# =========================
def save_data(rows):

    df = pd.DataFrame(rows)

    df = df.dropna(
        subset=["Date", "Ticker", "News_Text"]
    )

    df = df.drop_duplicates(
        subset=["Date", "Ticker", "News_Text"]
    )

    df = df.sort_values(
        ["Ticker", "Date"],
        ascending=[True, False]
    )

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    return df

# =========================
# MAIN
# =========================
def main():
    os.makedirs("data", exist_ok=True)

    all_rows = []
    date_ranges = generate_quarter_ranges(START_YEAR, END_YEAR)

    total_queries = (
        sum(len(keywords) for keywords in TICKERS_KEYWORDS.values())
        * len(date_ranges)
    )

    query_count = 0

    print("Mengambil berita...")

    for ticker, keywords in TICKERS_KEYWORDS.items():
        for keyword in keywords:
            for start_date, end_date in date_ranges:
                query_count += 1

                try:
                    rows = fetch_google_news(
                        keyword=keyword,
                        ticker=ticker,
                        start_date=start_date,
                        end_date=end_date
                    )

                    all_rows.extend(rows)

                    print(
                        f"{query_count}/{total_queries} | "
                        f"{ticker} | {keyword} | "
                        f"dapat {len(rows)}"
                    )

                    time.sleep(SLEEP_TIME)

                except Exception:
                    print(
                        f"{query_count}/{total_queries} | "
                        f"{ticker} | {keyword} | gagal"
                    )
                    time.sleep(0)

    final_df = save_data(all_rows)

    print("\nSelesai.")
    print(f"CSV berhasil dibuat: {OUTPUT_PATH}")
    print(f"Jumlah berita: {len(final_df)}")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
