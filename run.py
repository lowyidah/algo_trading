from data.data_feeds import YahooData
from main.strategy import TestStrategy
from main.backtest import BackTesting
from main.trading import Trading
from data.trading_platform import Alpaca
import pandas as pd

def main():
    # # Backtesting
    # backtest_msft_testStrategy = BackTesting(ticker='MSFT', strategy=TestStrategy(pd.Timedelta(1, "days"), 
    #     pd.Timedelta(1, "days")), data_feed=YahooData(),
    #     historical_period=pd.Timedelta(30, "days"), funds=0)
    # backtest_msft_testStrategy.run()
    # backtest_msft_testStrategy.evaluate_results('trades')
    # backtest_msft_testStrategy.plot_results('line')

    # Live trading
    live_testStrategy = Trading(ticker='MSFT', strategy=TestStrategy(pd.Timedelta(1, "days"), 
        pd.Timedelta(1, "days")), trading_platform=Alpaca(), data_feed=YahooData())
    live_testStrategy.run()


if __name__ == "__main__":
    main()