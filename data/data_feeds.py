from dataclasses import dataclass
from nis import match
import yfinance as yf
import pandas as pd
from data.asset_data import BarData, RollingBarData

# Returns BarData of ticker for given period and interval from Yahoo
# Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk
# Valid periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
def get_bar_data_yahoo(ticker, period, interval) -> pd.core.frame.DataFrame:
    asset = yf.Ticker(ticker)
    hist = asset.history(period=period, interval=interval)
    if interval == '1m':
        interval_seconds = 60
    elif interval == '2m':
        interval_seconds = 120
    elif interval == '5m':
        interval_seconds = 300
    elif interval == '15m':
        interval_seconds = 900
    elif interval == '30m':
        interval_seconds = 1800
    elif interval == '60m':
        interval_seconds = 3600
    elif interval == '90m':
        interval_seconds = 5400
    elif interval == '1h':
        interval_seconds = 3600
    elif interval == '1d':
        interval_seconds = 86400
    elif interval == '5d':
        interval_seconds = 432000
    elif interval == '1wk':
        interval_seconds = 604800

    # Convert hist to BarData input format
    yahoo_bar_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=pd.to_datetime([]))
    for date_time, price_volume_entry in hist.iterrows():
        if date_time.tzinfo is not None:
            naive_date_time = date_time.tz_convert(None)
        else:
            naive_date_time = date_time
        yahoo_bar_data.loc[naive_date_time] = price_volume_entry[['Open', 'High', 'Low', 'Close', 'Volume']]
        
    asset_data = BarData(interval_seconds, yahoo_bar_data)
    return asset_data
