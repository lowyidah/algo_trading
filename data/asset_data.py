from typing import List
import pandas as pd


# Base storage class for asset data for a time period
class BarData:
    def __init__(self, interval: pd.Timedelta = None, price_volume: pd.core.frame.DataFrame = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'], index=pd.to_datetime([]))) -> None:
        # price_volume is pandas dataframe with columns=['Open', 'High', 'Low', 'Close', 'Volume'] and index=pd.to_datetime([]). DateTimeIndex is timezone naive and in UTC timezone
        # To add: check invariant where interval between rows is the same as self.interval_
        self.price_volume_ = price_volume
        # interval_ stores the interval between each time period in seconds
        self.interval_ = interval
        
    # Sets interval between time periods in seconds
    def set_interval(self, interval: pd.Timedelta) -> None:
        self.interval_ = interval

    # price_volume is pandas dataframe with columns=['Open', 'High', 'Low', 'Close', 'Volume'] and index=pd.to_datetime([]) and sets 
    # self.price_volume_
    # To add: check invariant where interval between rows is the same as self.interval_
    def set_price_volume(self, price_volume) -> None:
        self.price_volume_ = price_volume.copy()

    # Returns pandas dataframe with columns=['Open', 'High', 'Low', 'Close', 'Volume'] and index=pd.to_datetime([])
    def get_price_volume(self) -> pd.core.frame.DataFrame:
        return self.price_volume_

    # Returns pandas series with labels=['Open', 'High', 'Low', 'Close', 'Volume'] of price_volume_entry at date_time_index
    def get_price_volume_entry(self, date_time_index: pd.Timestamp) -> pd.Series:
        return self.price_volume_.loc[date_time_index]

    # Returns list of all DateTimes of price_volume entries
    def get_date_times(self) -> list:
        return self.price_volume_.index

    # Returns list of (DateTimeIndex, pd.Series) pairs
    def get_date_time_price_volume_entry_pairs(self) -> list:
        return self.price_volume_.iterrows()

    # Returns interval between time periods in seconds
    def get_interval(self) -> pd.Timedelta:
        return self.interval_

    # Returns last closing price
    def get_last_closing_price(self) -> float:
        return self.price_volume_['Close'].iloc[-1]

    # Returns number of entries in price_volume
    def __len__(self) -> int:
        return self.price_volume_.shape[0]

    # price_volumn_entry is a list with ['Open', 'High', 'Low', 'Close', 'Volume'] and 
    # date_time is the index where price_volumn_entry is stored
    # To add: check invariant where interval between rows is the same as self.interval_
    def add_price_volume_entry(self, date_time: pd.Timestamp, price_volumn_entry: list) -> None:
        self.price_volume_.loc[date_time] = price_volumn_entry


    