from abc import ABC, abstractmethod
from typing import List
from data.asset_data import BarData, RollingBarData


# Strategy base class
class Strategy(ABC):
    # Set any snapshot of rolling_bar_data (ends just before current time period)
    def set_snapshot(self, rolling_bar_data: RollingBarData, funds: float, num_shares_held: int) -> None:
        self.rolling_bar_data_ = rolling_bar_data
        self.funds_ = funds
        self.num_shares_held_ = num_shares_held

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
    def get_action_volume(self, price) -> tuple:
        if len(self.rolling_bar_data_) == 0:
            return "hold", 1
        elif price > self.rolling_bar_data_.get_last_closing_price():
            return "buy", 1
        else:
            return "sell", 1

    def get_name(self) -> str:
        return 'test_strategy'


