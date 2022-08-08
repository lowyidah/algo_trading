import alpaca_trade_api as api
from alpaca_trade_api.stream import Stream
import os
from abc import ABC, abstractmethod
from data.trades import Trades



class Platform(ABC):
    def __init__(self) -> None:
        super().__init__()

    # types: market, limit, stop
    # Deletes all existing open orders of given ticker prior to current order being submitted
    @abstractmethod
    def submit_order(self, ticker: str, qty: int, side: str, type: str = "market", limit_price: float = None, stop_price: float = None):
        pass

    # Returns cash on hand after subtracting unexecuted "buy" orders (aka worst case scenario)
    @abstractmethod
    def get_funds_guaranteed(self) -> float:
        pass

    # Returns Trades of given ticker
    @abstractmethod
    def get_trades(self, ticker: str) -> Trades:
        pass

    # Returns number of shares of given tickers held (currently owned, not including unexecuted orders "buy" orders but including unexecuted "sell" orders)
    @abstractmethod
    def get_num_shares_guaranteed(self, ticker: str) -> int:
        pass

    # Returns last traded price of a given ticker
    @abstractmethod
    def get_last_traded_price(self, ticker: str) -> float:
        pass

class Alpaca(Platform):
    def __init__(self) -> None:
        super().__init__()
        api_key = os.environ.get('alpaca_api_key')
        api_secret = os.environ.get('alpaca_api_secret')
        base_url = "https://paper-api.alpaca.markets"
        self.alpaca_ = api.REST(api_key, api_secret, base_url)
        data_feed = "iex" # Change to "sip" if using paid subscription
        self.stream_ = Stream(api_key,
                        api_secret,
                        base_url=base_url,
                        data_feed=data_feed)
        self.stream_started_ = False
        self.live_data_ = {}
    
    # types: market, limit, stop
    # https://alpaca.markets/docs/api-references/trading-api/orders/
    # https://colab.research.google.com/drive/1ofIXDspe4LNXH7CXfArxOZuIOoAg1Uak?usp=sharing#scrollTo=Xy5Syxraoa5p
    # https://pypi.org/project/alpaca-trade-api/
    def submit_order(self, ticker: str, qty: int, side: str, type: str = "market", limit_price: float = None, stop_price: float = None):
        # Cancel all open orders of given ticker
        order_ids = []
        orders = self.alpaca_.list_orders(status='open', symbols=[ticker])
        for order in orders:
            order_ids.append(order['order_id'])
        for order_id in order_ids:
            self.alpaca_.cancel_order(order_id)

        # Place new order
        self.alpaca_.submit_order(ticker, qty=qty, side=side, type=type, limit_price=limit_price, stop_price=stop_price)

    def get_funds_guaranteed(self) -> float:
        _, value_of_open_buy_orders = self.get_open_order_info('buy')
        account = self.alpaca_.get_account()
        return (account['cash'] - value_of_open_buy_orders)

    def get_trades(self, ticker: str) -> Trades:
        trades = Trades()
        # list_orders(status=None, limit=None, after=None, until=None, direction=None, params=None,nested=None, symbols=None, side=None)
        orders = self.alpaca_.list_orders(status='closed', symbols=[ticker])
        for order in orders:
            trades.add_trade(order['filled_at'], order['side'], order['filled_qty'], order['filled_avg_price'])
        return trades

    def get_num_shares_guaranteed(self, ticker: str) -> int:
        quantity_of_open_orders, _ = self.get_open_order_info('sell', [ticker])
        position = self.alpaca_.get_position(ticker)
        return (position['qty_available'] - quantity_of_open_orders)


    def get_last_traded_price(self, ticker: str) -> float:
        if self.stream_started_== False:
            self.run_stream_on_ticker(ticker)
        live_data = self.live_data_.get(ticker)
        if live_data:
            return live_data.get('p')
        return None

    # Private 

    # Starts running self.stream_ on ticker
    # https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/realtime/
    def run_stream_on_ticker(self, ticker: str) -> float:
        self.stream_started_ = True
        async def trades_callback(data):
            self.live_data_[ticker] = data
        self.stream_.subscribe_trades(trades_callback, ticker)
        self.stream_.run()

    # Filters orders by side ("buy" / "sell")
    # Only works for stop orders or limit orders
    # Returns quantity of open orders and value of open orders
    def get_open_order_info(self, side: str, tickers_list: list = None) -> tuple:
        orders = self.alpaca_.list_orders(status='open', symbols=tickers_list, side=side)
        quantity = 0
        value = 0
        for order in orders:
            quantity += (order['qty'] - order['filled_qty'])
            if order['type'] == 'limit':
                value += order['limit_price']
            elif order['type'] == 'stop':
                value += order['stop_price']
        return quantity, value 