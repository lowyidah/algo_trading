from cmath import nan
from datetime import date
from data.asset_data import BarData, RollingBarData
from main.strategy import Strategy
import mplfinance as mpf
import pandas as pd
from matplotlib import pyplot as plt
from data.trades import trades
from results.plot import Plot
from results.evaluate import Evaluate
import os


# Each BackTesting instance should be used to test a given strategy over a given time period
class BackTesting:
    def __init__(self, stock_name: str, historical_bar_data: BarData, strategy: Strategy, funds: float = 0) -> None:
        self.stock_name_ = stock_name
        self.historical_bar_data_ = historical_bar_data
        self.strategy_ = strategy
        # Stores snapshot of bar data at a point in time, initially zero data
        self.rolling_bar_data_ = RollingBarData(interval=historical_bar_data.get_interval())
        self.num_shares_held_ = 0
        self.funds_ = funds
        # Stores trades made. Initially zero trades made
        self.trades_= trades()
        self.output_dir_ = 'out/' + self.stock_name_ + '/'


    # Iterates through entire historical_bar_data to simulate running of strategy
    def run(self) -> None:
        for date_time, price_volume_entry in self.historical_bar_data_.get_date_time_price_volume_entry_pair():
            current_price = price_volume_entry['Close']
            # Execute strategy at given point in time with given price
            self.strategy_.set_snapshot(self.rolling_bar_data_, self.funds_, self.num_shares_held_)
            action, num_shares = self.strategy_.get_action_volume(current_price)
            if action == "buy":
                self.num_shares_held_ += num_shares
                self.funds_ -= current_price * num_shares
                self.trades_.add_trade(date_time, "buy", num_shares, current_price)
            elif action == "sell":
                self.num_shares_held_ -= num_shares
                self.funds_ += current_price * num_shares
                self.trades_.add_trade(date_time, "sell", num_shares, current_price)
            elif action == "hold":
                pass
            else:
                print("Error: Invalid action")
            # Progress forward in time by adding one price_volume_entry to rolling_bar_data_
            self.rolling_bar_data_.add_price_volume_entry(date_time, price_volume_entry)    
    
    # Evaluates results of backtest
    # *args specify additional results to print, refer to Results class in results.py for list of possible additional results
    def evaluate_results(self, *args) -> None:
        Evaluate(self.output_dir(), self.historical_bar_data_, self.trades_, self.funds_, *args)
  
    # Plots results
    # type includes 'line', 'candle', 'ohlc', 'line', 'renko', 'pnf'
    # *args specify additional plots on to main plots, refer to Plotting class in plotting.py for list of possible additional plots
    def plot_results(self, type: str, *args) -> None:
        Plot(self.output_dir(), self.historical_bar_data_, type, self.trades_, *args)


    # Private members

    # Returns output directory and creates it if it does not yet exist
    def output_dir(self) -> str:
        isExist = os.path.exists(self.output_dir_)
        if not isExist:
            os.makedirs(self.output_dir_)
        return self.output_dir_
