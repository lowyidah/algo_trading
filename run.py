from data.data_feeds import YahooData
from main.strategy import TestStrategy
from main.backtest import BackTesting
import pandas as pd

def main():
    backtest_msft_testStrategy = BackTesting(ticker='MSFT', strategy=TestStrategy(pd.Timedelta(1, "days"), 
        pd.Timedelta(1, "days")), data_feed=YahooData(),
        historical_period=pd.Timedelta(30, "days"), funds=0)
    backtest_msft_testStrategy.run()
    backtest_msft_testStrategy.evaluate_results('trades')
    backtest_msft_testStrategy.plot_results('line')

if __name__ == "__main__":
    main()