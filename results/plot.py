import mplfinance as mpf
from data.asset_data import BarData
from data.trades import Trades
from matplotlib import pyplot as plt


class Plot:
    # type includes 'line', 'candle', 'ohlc', 'line', 'renko', 'pnf'
    # args include 
    def __init__(self, output_dir: str, historical_bar_data: BarData, type: str, trades: Trades = None, *args) -> None:
        self.historical_bar_data_ = historical_bar_data
        self.trades_ = trades
        self.additional_plots_ = []

        # Adding additional plots on to main plot
        if trades:
            self.add_trades()

        # Plotting and saving graph
        mpf.plot(self.historical_bar_data_.get_price_volume(), type=type, addplot=self.additional_plots_)
        plt.savefig(output_dir + 'backtest.png', dpi=500)


    def add_trades(self) -> None:
        buy_prices = []
        sell_prices = []

        for date_time_index in self.historical_bar_data_.get_date_times():
            buy_prices.append(float('nan'))
            sell_prices.append(float('nan'))
            trade = self.trades_.get_trade(date_time_index)
            if trade is not None:
                if trade["Action"] == "buy":
                    buy_prices[-1] = trade["Price"]
                elif trade["Action"] == "sell":
                    sell_prices[-1] = trade["Price"]

        self.additional_plots_.append(mpf.make_addplot(buy_prices, type='scatter', marker='X', markersize=50, color='g', linewidths=0.1))
        self.additional_plots_.append(mpf.make_addplot(sell_prices, type='scatter', marker='X', markersize=50, color='r', linewidths=0.1))
        

        
    