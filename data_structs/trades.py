import pandas as pd

class Trades:
    def __init__(self, trades: pd.core.frame.DataFrame = pd.DataFrame(columns=["Action", "Number", "Price"], index=pd.to_datetime([]))) -> None:
        # trades is pandas dataframe with columns=["Action", "Number", "Price"] and index=pd.to_datetime([]). DateTimeIndex is timezone naive and in UTC timezone
        # "Action" column can be "buy", "sell", or "hold"
        self.trades_ = trades

    # Returns trade history as a pandas dataframe with columns=["Action", "Number", "Price"] and index=pd.to_datetime([]). DateTimeIndex is timezone naive and in UTC timezone
    def get_trades(self) ->  pd.core.frame.DataFrame:
        return self.trades_

    # Returns trade history as a pandas series with columns=["Action", "Number", "Price"]. date_time is timezone naive and in UTC timezone
    def get_trade(self, date_time: pd.Timestamp) ->  pd.core.frame.DataFrame:
        if date_time in self.trades_.index:
            return self.trades_.loc[date_time]
        else:
            return None

    # trade is a list with ["Action", "Number", "Price"] and 
    # date_time is the index where trade is stored
    def add_trade(self, date_time: pd.Timestamp, action, number, price) -> None:
        self.trades_.loc[date_time] = [action, number, price]

    # Returns (DateTimeIndex, pd.Series) pair
    def get_date_time_trade_entry_pair(self) -> tuple:
        return self.trades_.iterrows()

    # Returns DateTimeIndices
    def get_date_times(self) -> pd.DatetimeIndex:
        return self.trades_.index