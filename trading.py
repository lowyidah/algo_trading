from trading_platform import Platform
from data.asset_data import BarData
from main.strategy import Strategy
from data.trades import Trades
from results.plot import Plot
from results.evaluate import Evaluate
from data.data_feeds import DataFetching
import pandas as pd
import os



# Each BackTesting instance should be used to test a given strategy over a given time period
class Trading:
    def __init__(self, ticker: str, strategy: Strategy, trading_platform: Platform, data_feed: DataFetching) -> None:
        self.ticker_ = ticker
        self.strategy_ = strategy
        self.trading_platform_ = trading_platform
        self.data_feed_ = data_feed
        self.rolling_bar_data_ = data_feed.get_bar_data(ticker, strategy.get_history_duration(), strategy.get_interval())
        self.output_dir_ = 'out/live/' + self.ticker_ + '/' + strategy.get_name() + '/'


    # Iterates through entire historical_bar_data to simulate running of strategy
    def run(self) -> None:
        while True:
            # Update self.rolling_bar_data_ with latest price_volume_entry given strategy.interval
            # most_recent_bar_data only has a single price_volume_entry
            most_recent_bar_data = self.data_feed_.get_bar_data(self.ticker_, self.strategy_.get_interval(), self.strategy_.get_interval())
            most_recent_date_time, most_recent_price_volume_entry = most_recent_bar_data.get_date_time_price_volume_entry_pairs()[0]
            # Only if is new datetime then update self.rolling_bar_data and continue on to execute strategy
            last_date_time = self.rolling_bar_data_.get_date_times()[-1]
            if most_recent_date_time > last_date_time:
                self.rolling_bar_data_.add_price_volume_entry(most_recent_date_time, most_recent_price_volume_entry)
            else:
                # sleep()
                break
            
            # If reach this point, latest price_volume_entry in self.rolling_bar_data_ is new (unseen before)
            # To do: update current_price
            current_price = self.rolling_bar_data_.get_last_closing_price()
            # Execute strategy at given point in time with given price
            self.strategy_.set_snapshot(self.rolling_bar_data_, self.trading_platform_.get_funds_guaranteed(), self.trading_platform_.get_num_shares_guaranteed())
            action, num_shares, order_type, limit_price, stop_price = self.strategy_.get_action_volume(current_price)
            if action == "buy":
                self.trading_platform_.submit_order(self.ticker_, num_shares, "buy", order_type, limit_price, stop_price)
            elif action == "sell":
                self.trading_platform_.submit_order(self.ticker_, num_shares, "sell",  order_type, limit_price, stop_price)
            elif action == "hold":
                pass
            else:
                print("Error: Invalid action")
            


    # Evaluates results of trading
    # *args specify additional results to print, refer to Results class in results.py for list of possible additional results
    def evaluate_results(self, *args) -> None:
        Evaluate(self.output_dir(), self.get_historical_bar_data_spanning_trades(), self.trading_platform_.get_trades(self.ticker_), self.trading_platform_.get_funds_guaranteed(), *args)
  
    # Plots results trading
    # type includes 'line', 'candle', 'ohlc', 'line', 'renko', 'pnf'
    # *args specify additional plots on to main plots, refer to Plotting class in plotting.py for list of possible additional plots
    def plot_results(self, type: str, *args) -> None:
        Plot(self.output_dir(), self.get_historical_bar_data_spanning_trades(), type, self.trading_platform_.get_trades(self.ticker_), *args)


    # Returns output directory and creates it if it does not yet exist
    def output_dir(self) -> str:
        isExist = os.path.exists(self.output_dir_)
        if not isExist:
            os.makedirs(self.output_dir_)
        return self.output_dir_


    # Private

    # Returns historical_bar_data that spans start of self.trades_ to now
    def get_historical_bar_data_spanning_trades(self) -> BarData:
        first_trade_date_time = self.trading_platform_.get_trades(self.ticker_).get_date_times()[0]
        historical_time_delta = pd.Timestamp.now() - first_trade_date_time
        historical_bar_data = self.data_feed_.get_bar_data(self.ticker_, historical_time_delta, self.strategy_.get_interval())
        return historical_bar_data