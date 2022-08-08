from dataclasses import dataclass
from nis import match
import yfinance as yf
import pandas as pd
from data_structs.asset_data import BarData
from abc import ABC, abstractmethod



class DataFetching(ABC):
    def __init__(self) -> None:
        super().__init__()

    # Valid intervals are pd.Timedelta corresponding to: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk
    # Valid periods are pd.Timedelta corresponding to: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    @abstractmethod
    def get_bar_data(self, ticker: str, period: pd.Timedelta, interval: pd.Timedelta) -> BarData:
        pass
class YahooData(DataFetching):
    def __init__(self) -> None:
        super().__init__()

    def get_bar_data(self, ticker: str, period: pd.Timedelta, interval: pd.Timedelta) -> BarData:
        asset = yf.Ticker(ticker)
        hist = asset.history(period=self.timedelta_to_str_periods(period), interval=self.timedelta_to_str_intervals(interval))

        # Convert hist to BarData input format
        yahoo_bar_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=pd.to_datetime([]))
        for date_time, price_volume_entry in hist.iterrows():
            if date_time.tzinfo is not None:
                naive_date_time = date_time.tz_convert(None)
            else:
                naive_date_time = date_time
            yahoo_bar_data.loc[naive_date_time] = price_volume_entry[['Open', 'High', 'Low', 'Close', 'Volume']]
            
        asset_data = BarData(interval, yahoo_bar_data)
        return asset_data

    def timedelta_to_str_periods(self, timedelta: pd.Timedelta) -> str:
        days = timedelta.days
        if days > 3650:
            return 'max'
        elif days > 1825:
            return '10y'
        elif days > 730:
            return '5y'
        elif days > 365:
            return '2y'
        elif days > 182:
            return '1y'
        elif days > 91:
            return '6mo'
        elif days > 30:
            return '3mo'
        elif days > 5:
            return '1mo'
        elif days > 1:
            return '5d'
        else:
            return '1d'

    def timedelta_to_str_intervals(self, timedelta: pd.Timedelta) -> str:
        days = timedelta.days
        seconds = timedelta.seconds
        if days >= 7 and seconds > 0:
            print("Error: invalid interval")
        elif days >= 5 and seconds > 0:
            return '1wk'
        elif days >= 1 and seconds > 0:
            return '5d'
        elif days == 1 or seconds > 5400:
            return '1d'
        elif seconds > 3600:
            return '90m'
        elif seconds > 1800:
            return '60m'
        elif seconds > 900:
            return '30m'
        elif seconds > 300:
            return '15m'
        elif seconds > 120:
            return '5m'
        elif seconds > 60:
            return '2m'
        else:
            return '1m'
