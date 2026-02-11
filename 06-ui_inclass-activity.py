from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(layout='wide', page_title="Stock Analyzer")

# CONSTANTS
END = date.today()
START = END - timedelta(365)

# data handling
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start, end, auto_adjust=False)
        if data.empty:
            return None, f"No data found for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data, f"Successfully loaded data for {ticker}"
    except Exception as e:
        return None, f"Error {e}"

# sidebar
st.sidebar.title("🗠 Inputs")
ticker = st.sidebar.text_input("Stock symbol", value="AAPL").upper()
comparison_ticker = st.sidebar.text_input("Comparison symbol", value="SPY").upper()
col1, col2 = st.sidebar.columns(2)
start = col1.date_input("Start Date", value=START)
end = col2.date_input("End Date", value=END)
moving_average = st.sidebar.slider("Moving Average Window",
                                   min_value=10,
                                   max_value=100,
                                   value=50,
                                   step=5)
run = st.sidebar.button("Run Analysis", type='primary')




#main UI
st.title("Stock Analyzer")

if run:
    with st.spinner(f"Fetching {ticker} and {comparison_ticker} data..."):
        df, message = get_stock_data(ticker, start, end)
        comparison_df, comparison_message = get_stock_data(comparison_ticker, start, end)

    if df is not None:
        st.sidebar.success(message)
    else:
        st.sidebar.error(message)

    if comparison_df is not None:
        st.sidebar.success(comparison_message)
    else:
        st.sidebar.error(comparison_message)

    if df is None or comparison_df is None:
        st.stop()


    df['MA'] = df['Close'].rolling(window=moving_average).mean()
    df['pct_change'] = df['Close'].pct_change() * 100

    df["normalized_close"] = (df["Close"] / df["Close"].iloc[0]) * 100
    comparison_df["normalized_close"] = (comparison_df["Close"] / comparison_df["Close"].iloc[0]) * 100


    # output
    tab1, tab2, tab3, tab4 = st.tabs(['📉 Chart', '📊 Statistics', '🗄️ Raw Data', '📈 Comparison'])
    with tab1:
        st.subheader(f"{ticker} High Level Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Price", f"{df['Close'].iloc[-1]:.2f}")
        col2.metric("Cum Change", f"{((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100:.2f}")
        col3.metric("Trading Days", f"{len(df)}")

        figure = px.line(df, y= ['Close', 'MA'])
        figure.update_layout(hovermode='x unified')
        with st.spinner("Creating chart"):
            st.plotly_chart(figure, use_container_width=True)

    with tab2:
        st.subheader("Summary Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Daily Change Statistics**")
            summary = df['pct_change'].describe()
            st.dataframe(summary)
        with col2:
            price_stats = pd.DataFrame(
                {'Metric': ['High', 'Low', 'Mean', 'Volatility'],
                 'Values': [
                     f"{df['Close'].max()}",
                     f"{df['Close'].min()}",
                     f"{df['Close'].mean()}",
                     f"{df['Close'].std()}"
                 ]
                }
            )
            st.dataframe(price_stats)

    with tab3:
        st.subheader("Raw Data")
        st.dataframe(df.tail(10))
        csv = df.to_csv()
        st.download_button(
                           label="Download Data",
                           data = csv,
                           file_name = f"{ticker}_{start}_{end}.csv",
                           mime="text/csv"
                            )
    with tab4:
        st.subheader("Performance Comparison (Base 100)")

        # Align both series by date (inner join keeps only dates that exist for both)
        combined = pd.DataFrame({
        ticker: df["normalized_close"],
        comparison_ticker: comparison_df["normalized_close"]
        }).dropna()

        # Convert to long format for Plotly legend labels
        long_df = combined.reset_index().melt(
            id_vars=combined.index.name or "index",
            var_name="Ticker",
            value_name="Normalized Close"
        )

        # If index name is None, melt used "index" — rename it to Date for clarity
        if "index" in long_df.columns:
            long_df = long_df.rename(columns={"index": "Date"})
        else:
            long_df = long_df.rename(columns={combined.index.name: "Date"})

        fig = px.line(
            long_df,
            x="Date",
            y="Normalized Close",
            color="Ticker",
            title=f"{ticker} vs {comparison_ticker} Performance (Base 100)"
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Summary stats table for normalized values
        summary_stats = pd.DataFrame({
            "Ticker": [ticker, comparison_ticker],
            "Min": [combined[ticker].min(), combined[comparison_ticker].min()],
            "Max": [combined[ticker].max(), combined[comparison_ticker].max()],
            "Final": [combined[ticker].iloc[-1], combined[comparison_ticker].iloc[-1]],
        })

        st.write("### Summary (Normalized)")
        st.dataframe(summary_stats)

    