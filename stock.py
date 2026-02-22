import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sb
import yfinance as yf  # Assuming yfinance for data API

sb.set_theme()

"""
STUDENT CHANGE LOG & AI DISCLOSURE:
----------------------------------
1. Did you use an LLM (ChatGPT/Claude/etc.)? [Yes/No]
2. If yes, what was your primary prompt?
----------------------------------
"""

## Yes, I did use a landuage model to complete this assignment. I used ChatGPT to help me. I asked it to guide me throug hevery step of this assignment and how to work through each step explaining what each step does. 

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())


class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol.upper().strip()
        self.start = start
        self.end = end
        self.data = self.get_data()

    def get_data(self):
        """
        Downloads historical OHLCV data and stores it as a pandas DataFrame.
        Index is converted to pandas datetime and named 'Date'.
        Enriches data by calling calc_returns().
        """
        # yfinance 'end' is typically exclusive, so add 1 day to include the end date
        end_inclusive = (pd.to_datetime(self.end) + pd.Timedelta(days=1)).date().isoformat()

        df = yf.download(
            self.symbol,
            start=self.start,
            end=end_inclusive,
            progress=False,
            auto_adjust=False
        )

        if df is None or df.empty:
            raise ValueError(
                f"No data returned for symbol '{self.symbol}' between {self.start} and {self.end}."
            )

        # Ensure DatetimeIndex
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"

        # Standardize columns (yfinance sometimes returns multi-index columns in some situations)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Keep expected columns if present
        expected_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        keep_cols = [c for c in expected_cols if c in df.columns]
        df = df[keep_cols].copy()

        # Calculate returns-related columns
        self.calc_returns(df)

        return df

    def calc_returns(self, df):
        """
        Adds:
          - 'change': Close-to-close difference relative to previous day's close (absolute diff)
          - 'instant_return': daily log return (np.log(Close).diff().round(4))
        Requirement: Use vectorized pandas ops (no loops).
        """
        if "Close" not in df.columns:
            raise KeyError("DataFrame must contain a 'Close' column to compute returns.")

        df["change"] = df["Close"].diff()
        df["instant_return"] = np.log(df["Close"]).diff().round(4)

        return df

    def add_technical_indicators(self, windows=[20, 50]):
        """
        Add Simple Moving Averages (SMA) for the given windows
        to the internal DataFrame. Produce a plot showing the closing price and SMAs.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded. Cannot add technical indicators.")

        if "Close" not in self.data.columns:
            raise KeyError("DataFrame must contain 'Close' to compute moving averages.")

        # Add SMA columns
        for w in windows:
            col = f"SMA_{w}"
            self.data[col] = self.data["Close"].rolling(window=w, min_periods=w).mean()

        # Plot Close + SMAs
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.data.index, self.data["Close"], label="Close", linewidth=2)

        for w in windows:
            col = f"SMA_{w}"
            if col in self.data.columns:
                ax.plot(self.data.index, self.data[col], label=col, linewidth=1.5)

        ax.set_title(f"{self.symbol} Closing Price with Simple Moving Averages")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        plt.show()

        return fig, ax

    def plot_return_dist(self, bins=40):
        """Plot a well-formatted histogram of instantaneous returns."""
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded. Cannot plot return distribution.")

        if "instant_return" not in self.data.columns:
            raise KeyError("Missing 'instant_return'. Run get_data()/calc_returns() first.")

        returns = self.data["instant_return"].dropna()
        if returns.empty:
            raise ValueError("No instantaneous return data to plot (all NaN).")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(returns, bins=bins)
        ax.set_title(f"{self.symbol} Distribution of Daily Instantaneous Returns")
        ax.set_xlabel("Instantaneous Return (log)")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

        return fig, ax

    def plot_performance(self):
        """
        Plot a well-formatted line graph of the stock’s performance over the
        range of data collected, as a percent gain/loss from the first close.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded. Cannot plot performance.")

        if "Close" not in self.data.columns:
            raise KeyError("DataFrame must contain 'Close' to plot performance.")

        close = self.data["Close"].dropna()
        if close.empty:
            raise ValueError("No close data to plot.")

        perf_pct = (close / close.iloc[0] - 1) * 100

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(perf_pct.index, perf_pct.values, linewidth=2)
        ax.set_title(f"{self.symbol} Performance (% Gain/Loss)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Percent Gain/Loss")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

        return fig, ax


def main():
    # 1) Instantiate a test object
    aapl = Stock("AAPL")

    # 2) Access the data attribute
    print(aapl.data.head())

    # 3) Generate the plots required
    aapl.plot_return_dist()
    aapl.plot_performance()
    aapl.add_technical_indicators(windows=[20, 50])


if __name__ == "__main__":
    main()