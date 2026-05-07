import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------------
# CREATE FOLDERS
# -----------------------------------
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# -----------------------------------
# STOCK SETTINGS
# -----------------------------------
ticker = "AAPL"

start_date = "2023-01-01"

end_date = "2025-01-01"

# -----------------------------------
# FETCH STOCK DATA
# -----------------------------------
print("Fetching stock market data...")

df = yf.download(
    ticker,
    start=start_date,
    end=end_date
)

# -----------------------------------
# FIX MULTI-INDEX COLUMNS
# -----------------------------------
if isinstance(df.columns, pd.MultiIndex):

    df.columns = df.columns.get_level_values(0)

# -----------------------------------
# CHECK DATA
# -----------------------------------
if df.empty:

    print("No data found.")

else:

    print("Data fetched successfully!")

    # Reset index
    df.reset_index(inplace=True)

    # Save CSV
    file_path = f"data/{ticker}_stock_data.csv"

    df.to_csv(file_path, index=False)

    print(f"CSV saved at: {file_path}")

    # -----------------------------------
    # DATA CLEANING
    # -----------------------------------
    print("\nCleaning data...")

    # Convert numeric columns safely
    numeric_cols = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Remove missing values
    df.dropna(inplace=True)

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    print("Data cleaned successfully!")

    # -----------------------------------
    # DAILY RETURNS
    # -----------------------------------
    print("\nCalculating daily returns...")

    df["Daily Return"] = df["Close"].pct_change()

    # -----------------------------------
    # MOVING AVERAGES
    # -----------------------------------
    df["MA20"] = df["Close"].rolling(window=20).mean()

    df["MA50"] = df["Close"].rolling(window=50).mean()

    # -----------------------------------
    # VOLATILITY
    # -----------------------------------
    volatility = df["Daily Return"].std()

    # -----------------------------------
    # PRICE ANALYSIS
    # -----------------------------------
    highest_price = df["High"].max()

    lowest_price = df["Low"].min()

    average_close = df["Close"].mean()

    total_days = len(df)

    # -----------------------------------
    # PRINT RESULTS
    # -----------------------------------
    print("\n📈 STOCK ANALYSIS RESULTS")

    print(f"\nTicker: {ticker}")

    print(f"Highest Price: {round(highest_price, 2)}")

    print(f"Lowest Price: {round(lowest_price, 2)}")

    print(f"Average Closing Price: {round(average_close, 2)}")

    print(f"Volatility: {round(volatility, 4)}")

    print(f"Total Trading Days: {total_days}")

    # -----------------------------------
    # SAVE REPORT
    # -----------------------------------
    report_path = f"reports/{ticker}_summary_report.txt"

    with open(report_path, "w") as file:

        file.write("STOCK MARKET ANALYSIS REPORT\n")
        file.write("============================\n\n")

        file.write(f"Ticker: {ticker}\n")
        file.write(f"Highest Price: {round(highest_price, 2)}\n")
        file.write(f"Lowest Price: {round(lowest_price, 2)}\n")
        file.write(f"Average Closing Price: {round(average_close, 2)}\n")
        file.write(f"Volatility: {round(volatility, 4)}\n")
        file.write(f"Total Trading Days: {total_days}\n")

    print(f"\nReport saved at: {report_path}")

    # -----------------------------------
    # VISUALIZATION
    # -----------------------------------
    print("\nGenerating charts...")

    # -----------------------------------
    # STOCK CLOSING PRICE CHART
    # -----------------------------------
    plt.figure(figsize=(12, 6))

    plt.plot(df["Date"], df["Close"])

    plt.title(f"{ticker} Closing Price")

    plt.xlabel("Date")

    plt.ylabel("Closing Price")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"outputs/{ticker}_closing_price.png")

    plt.close()

    # -----------------------------------
    # MOVING AVERAGE CHART
    # -----------------------------------
    plt.figure(figsize=(12, 6))

    plt.plot(
        df["Date"],
        df["Close"],
        label="Close Price"
    )

    plt.plot(
        df["Date"],
        df["MA20"],
        label="20-Day MA"
    )

    plt.plot(
        df["Date"],
        df["MA50"],
        label="50-Day MA"
    )

    plt.title(f"{ticker} Moving Averages")

    plt.xlabel("Date")

    plt.ylabel("Price")

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"outputs/{ticker}_moving_average.png")

    plt.close()

    # -----------------------------------
    # DAILY RETURNS CHART
    # -----------------------------------
    plt.figure(figsize=(12, 6))

    plt.plot(df["Date"], df["Daily Return"])

    plt.title(f"{ticker} Daily Returns")

    plt.xlabel("Date")

    plt.ylabel("Daily Return")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"outputs/{ticker}_daily_returns.png")

    plt.close()

    # -----------------------------------
    # VOLUME CHART
    # -----------------------------------
    plt.figure(figsize=(12, 6))

    plt.bar(df["Date"], df["Volume"])

    plt.title(f"{ticker} Trading Volume")

    plt.xlabel("Date")

    plt.ylabel("Volume")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"outputs/{ticker}_volume_chart.png")

    plt.close()

    print("Charts generated successfully!")

    # -----------------------------------
    # DISPLAY DATA
    # -----------------------------------
    print("\nStock Data Preview:\n")

    print(df.head())