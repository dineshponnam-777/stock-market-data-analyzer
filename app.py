import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Stock Market Data Analyzer",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📈 Stock Market Data Analyzer Dashboard")

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.header("Stock Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    value="AAPL"
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2023-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    value=pd.to_datetime("2025-01-01")
)

# -----------------------------------
# FETCH DATA
# -----------------------------------
st.write("Fetching stock market data...")

df = yf.download(
    ticker,
    start=start_date,
    end=end_date
)

# -----------------------------------
# CHECK DATA
# -----------------------------------
if df.empty:

    st.error("No stock data found.")

else:

    st.success("Data fetched successfully!")

    # -----------------------------------
    # RESET INDEX
    # -----------------------------------
    df.reset_index(inplace=True)

    # -----------------------------------
    # FIX MULTI-INDEX COLUMNS
    # -----------------------------------
    if isinstance(df.columns, pd.MultiIndex):

        df.columns = df.columns.get_level_values(0)

    # -----------------------------------
    # CLEAN DATA
    # -----------------------------------
    df.dropna(inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])

    # -----------------------------------
    # DAILY RETURNS
    # -----------------------------------
    df["Daily Return"] = df["Close"].pct_change()

    # -----------------------------------
    # MOVING AVERAGES
    # -----------------------------------
    df["MA20"] = df["Close"].rolling(window=20).mean()

    df["MA50"] = df["Close"].rolling(window=50).mean()

    # -----------------------------------
    # KPI CALCULATIONS
    # -----------------------------------
    highest_price = round(df["High"].max().item(), 2)

    lowest_price = round(df["Low"].min().item(), 2)

    average_close = round(df["Close"].mean().item(), 2)

    volatility = round(df["Daily Return"].std().item(), 4)

    latest_close = round(df["Close"].iloc[-1].item(), 2)

    total_volume = int(df["Volume"].sum())

    # -----------------------------------
    # KPI SECTION
    # -----------------------------------
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Price",
        highest_price
    )

    col2.metric(
        "Lowest Price",
        lowest_price
    )

    col3.metric(
        "Average Close",
        average_close
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Volatility",
        volatility
    )

    col5.metric(
        "Latest Close",
        latest_close
    )

    col6.metric(
        "Total Volume",
        f"{total_volume:,}"
    )

    # -----------------------------------
    # CLOSING PRICE CHART
    # -----------------------------------
    st.subheader("📈 Closing Price Trend")

    fig_close = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker} Closing Price Trend"
    )

    st.plotly_chart(
        fig_close,
        use_container_width=True
    )

    # -----------------------------------
    # MOVING AVERAGE CHART
    # -----------------------------------
    st.subheader("📉 Moving Average Analysis")

    fig_ma = go.Figure()

    fig_ma.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode='lines',
            name='Close Price'
        )
    )

    fig_ma.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA20"],
            mode='lines',
            name='20-Day MA'
        )
    )

    fig_ma.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA50"],
            mode='lines',
            name='50-Day MA'
        )
    )

    fig_ma.update_layout(
        title=f"{ticker} Moving Average Analysis",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    st.plotly_chart(
        fig_ma,
        use_container_width=True
    )

    # -----------------------------------
    # DAILY RETURNS CHART
    # -----------------------------------
    st.subheader("📊 Daily Returns")

    fig_returns = px.line(
        df,
        x="Date",
        y="Daily Return",
        title=f"{ticker} Daily Returns"
    )

    st.plotly_chart(
        fig_returns,
        use_container_width=True
    )

    # -----------------------------------
    # TRADING VOLUME CHART
    # -----------------------------------
    st.subheader("📦 Trading Volume")

    fig_volume = px.bar(
        df,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume"
    )

    st.plotly_chart(
        fig_volume,
        use_container_width=True
    )

    # -----------------------------------
    # STOCK DATA TABLE
    # -----------------------------------
    st.subheader("📋 Stock Market Dataset")

    st.dataframe(df)

    # -----------------------------------
    # DOWNLOAD CSV
    # -----------------------------------
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name=f"{ticker}_stock_data.csv",
        mime="text/csv"
    )

    # -----------------------------------
    # FINAL SUCCESS MESSAGE
    # -----------------------------------
    st.success("Dashboard generated successfully!")