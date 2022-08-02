import alpaca_trade_api as api
import os
from abc import ABC, abstractmethod
import pandas as pd
from data.trades import Trades



class LiveTrade:
    # types: market, limit, stop
    @abstractmethod
    def submit_order(self, symbol: str, qty: int, side: str, type: str = "market", limit_price: float = None, stop_price: float = None):
        pass

    # Returns cash on hand
    @abstractmethod
    def get_funds(self) -> float:
        pass

    # Returns historical Trades of given symbol
    @abstractmethod
    def get_trades(self, symbol: str) -> Trades:
        pass

    # Returns number of shares of given symbols held
    def get_num_shares(self, symbol: str) -> int:
        pass


class AlpacaTrade(LiveTrade):
    def __init__(self) -> None:
        api_key = os.environ.get('alpaca_api_key')
        api_secret = os.environ.get('alpaca_api_secret')
        base_url = "https://paper-api.alpaca.markets"
        self.alpaca_ = api.REST(api_key, api_secret, base_url)
    
    # types: market, limit, stop
    # https://alpaca.markets/docs/api-references/trading-api/orders/
    # https://colab.research.google.com/drive/1ofIXDspe4LNXH7CXfArxOZuIOoAg1Uak?usp=sharing#scrollTo=Xy5Syxraoa5p
    def submit_order(self, symbol: str, qty: int, side: str, type: str = "market", limit_price: float = None, stop_price: float = None):
        self.alpaca_.submit_order(symbol, qty=qty, side=side, type=type, limit_price=limit_price, stop_price=stop_price)

    def get_funds(self) -> float:
        account = self.alpaca_.get_account()
        return account['cash']

    def get_trades(self, symbol: str) -> Trades:
        trades = Trades()
        orders = self.alpaca_.get_orders()
        for order in orders:
            if order['filled_at'] and order['symbol'] == symbol:
                trades.add_trade(order['filled_at'], order['side'], order['filled_qty'], order['filled_avg_price'])
        return trades

    def get_num_shares(self, symbol: str) -> int:
        position = self.alpaca_.get_position(symbol)
        return position['qty_available']