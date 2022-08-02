import sys
from data.asset_data import BarData
from data.trades import trades


class Evaluate:
    # type includes 'line', 'candle', 'ohlc', 'line', 'renko', 'pnf'
    # args include 'trades', 
    def __init__(self, output_dir: str, historical_bar_data: BarData, trades: trades = None, funds: int = 0, *args) -> None:
        self.historical_bar_data_ = historical_bar_data
        self.trades_ = trades
        self.funds_ = funds
        self.num_shares_held_ = 0
        for _, trade in trades.get_date_time_trade_entry_pair():
            if trade["Action"] == "buy":
                self.num_shares_held_ += trade["Number"]
            elif trade["Action"] == "sell":
                self.num_shares_held_ -= trade["Number"]

        # Print results to a text file
        original_stdout = sys.stdout # Save a reference to the original standard output
        with open(output_dir + 'results.txt', 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.

            # Print standard results
            latest_price = self.historical_bar_data_.get_last_closing_price()
            value_of_shares_held = latest_price * self.num_shares_held_
            net_worth = value_of_shares_held + self.funds_
            print("Net worth: " + str(net_worth))
            print("Cash on hand: " + str(self.funds_)) 
            print("Number of shares owned: " +str(self.num_shares_held_))
            print("Value of shares held: " + str(value_of_shares_held))
            print("Latest price of share: " + str(latest_price))

            # Printing additional results
            if 'trades' in args:
                print(self.trades_.get_trades())

            sys.stdout = original_stdout # Reset the standard output to its original value


       
        

        
    