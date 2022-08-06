from platform import Platform, Alpaca
from data.asset_data import BarData, RollingBarData
from main.strategy import Strategy
from data.trades import Trades
from results.plot import Plot
from results.evaluate import Evaluate
import os




# Each BackTesting instance should be used to test a given strategy over a given time period
class Trading:
    def __init__(self, stock_name: str, strategy: Strategy, trading_platform: Platform) -> None:
        self.stock_name_ = stock_name
        self.strategy_ = strategy
        self.trading_platform_ = trading_platform
        self.trades_ = trading_platform.get_historical_trades()


    # Iterates through entire historical_bar_data to simulate running of strategy
    def run(self) -> None:
        while True:


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
