import os
import pandas as pd
import yfinance as yf

# =========================
# SETTING
# =========================
START_DATE = "2024-01-01"
END_DATE = "2026-05-01"

TICKERS = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK"]

# =========================
# 1. LOAD NEWS
# =========================
news = pd.read_csv("data/berita.csv")

news["Date"] = pd.to_datetime(news["Date"]).dt.date
news["Ticker"] = news["Ticker"].astype(str)
news["News_Text"] = news["News_Text"].astype(str)

# =========================
# 2. SENTIMENT SCORE
# =========================
def sentiment_score(text):
    text = text.lower()

    positive_words = [
        "naik", "menguat", "tumbuh", "laba", "untung", "positif",
        "rekor", "buyback", "dividen", "optimistis", "ekspansi",
        "cemerlang", "undervalued", "prospek", "meningkat"
    ]

    negative_words = [
        "turun", "melemah", "anjlok", "ambruk", "rugi", "negatif",
        "tekanan", "terkoreksi", "net sell", "jual", "merosot",
        "perlambatan", "risiko", "beban"
    ]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return 0.6
    elif score < 0:
        return -0.6
    else:
        return 0.0


news["Sentiment_Score"] = news["News_Text"].apply(sentiment_score)

# =========================
# 3. DOWNLOAD STOCK DATA
# =========================
all_stock = []

for ticker in TICKERS:
    print(f"Download data saham: {ticker}")

    stock = yf.download(
        ticker,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False
    )

    stock = stock.reset_index()

    # Fix kolom MultiIndex dari yfinance
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    stock = stock[["Date", "Close", "Volume"]]
    stock["Date"] = pd.to_datetime(stock["Date"]).dt.date
    stock["Ticker"] = ticker

    all_stock.append(stock)

stock_df = pd.concat(all_stock, ignore_index=True)

# =========================
# 4. BUAT TARGET LABEL DARI DATA SAHAM
# =========================
stock_df = stock_df.sort_values(["Ticker", "Date"])

stock_df["Next_Close"] = stock_df.groupby("Ticker")["Close"].shift(-1)

stock_df["Target_Label"] = (
    stock_df["Next_Close"] > stock_df["Close"]
).astype(int)

stock_df = stock_df.drop(columns=["Next_Close"])

# =========================
# 5. MERGE NEWS + STOCK
# =========================
final_df = pd.merge(
    news,
    stock_df,
    on=["Date", "Ticker"],
    how="inner"
)

# =========================
# 6. SUSUN KOLOM FINAL
# =========================
final_df = final_df[
    [
        "Date",
        "Ticker",
        "News_Text",
        "Sentiment_Score",
        "Close",
        "Volume",
        "Target_Label"
    ]
]

# Rename sesuai bahasa Indonesia
final_df = final_df.rename(columns={
    "Date": "Tanggal",
    "News_Text": "Teks_Berita",
    "Sentiment_Score": "Nilai_Sentimen",
    "Close": "Harga_Penutupan_Saham"
})

# =========================
# 7. SIMPAN OUTPUT
# =========================
os.makedirs("output", exist_ok=True)

final_df.to_csv("output/final_dataset.csv", index=False)

print("\nDATASET FINAL BERHASIL DIBUAT")
print("Jumlah data:", len(final_df))

print("\nDistribusi Target_Label:")
print(final_df["Target_Label"].value_counts())

print("\nPreview data:")
print(final_df.head())
