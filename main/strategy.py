from abc import ABC, abstractmethod
from typing import List
from data.asset_data import BarData, RollingBarData
import pandas as pd


# Strategy base class
class Strategy(ABC):
    # interval is the time gap between two BarData price_volume entries
    # history_duration is the amount of BarData price_colume entries needed for the strategy to work, measured in time
    def __init__(self, interval: pd.Timedelta, history_duration: pd.Timedelta) -> None:
        super().__init__()
        self.interval_ = interval
        self.history_duration_ = history_duration

    # Set any snapshot of rolling_bar_data (ends just before current time period)
    def set_snapshot(self, rolling_bar_data: RollingBarData, funds: float, num_shares_held: int) -> None:
        if rolling_bar_data.get_interval() != self.interval_:
            print("Error: Strategy interval and BarData interval do not match")
        self.rolling_bar_data_ = rolling_bar_data
        self.funds_ = funds
        self.num_shares_held_ = num_shares_held

    def get_interval(self) -> pd.Timedelta:
        return self.interval_

    def get_history_duration(self) -> pd.Timedelta:
        return self.history_duration_

    # Override this method in actual strategy to define actual strategy
    # Return format is a tuple("buy" / "sell" / "hold", number of shares)
    # Decide whether to buy / sell / hold given snapshot (where last entry of rolling_bar_data is one before current time) and current price
    @abstractmethod
    def get_action_volume(self, price) -> tuple:
        pass

    # Override this method in actual strategy to define actual strategy name
    @abstractmethod
    def get_name(self) -> tuple:
        pass



# Define strategies by inheriting from Strategy base class and overidding get_buy_sell_volume() abstract method
class TestStrategy(Strategy):
    def __init__(self, interval: pd.Timedelta, history_duration: pd.Timedelta) -> None:
        super().__init__(interval, history_duration)

    def get_action_volume(self, price) -> tuple:
        if len(self.rolling_bar_data_) == 0:
            return "hold", 1
        elif price > self.rolling_bar_data_.get_last_closing_price():
            return "buy", 1
        else:
            return "sell", 1

    def get_name(self) -> str:
        return 'test_strategy'


