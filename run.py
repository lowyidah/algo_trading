from data.data_feeds import get_bar_data_yahoo
from main.strategy import TestStrategy
from main.backtest import BackTesting

def main():
    bar_data_msft = get_bar_data_yahoo('MSFT', '1mo', '1d')
    backtest_msft_testStrategy = BackTesting('MSFT', bar_data_msft, TestStrategy(), 0)
    backtest_msft_testStrategy.run()
    backtest_msft_testStrategy.evaluate_results('trades')
    backtest_msft_testStrategy.plot_results('line')

if __name__ == "__main__":
    main()