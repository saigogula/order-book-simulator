from dataclasses import dataclass
from collections import deque
import itertools
import random
import matplotlib.pyplot as plt


@dataclass
class Order:
    id: int
    side: str
    order_type: str
    quantity: int
    price:  float | None = None

    def __str__(self):
        if self.order_type == 'market':
            return f"#{self.id} {self.side.upper()} MARKET {self.quantity}"
        return f"{self.id} {self.side.upper()} {self.quantity} @ ${self.price}"
    
@dataclass
class Trade:
    buy_order_id: int
    sell_order_id: int
    quantity: int
    price: float

    def __str__(self):

        return (
            f"TRADE: buy #{self.buy_order_id} "
            f"sells to #{self.sell_order_id}, "
            f"{self.quantity} shares @ ${self.price}"
        )
class OrderBook:
    def __init__(self):
        self.buys = []
        self.sells = []
        self.trades = []
        self.price_history = []
        self.order_ids = itertools.count(1)

    def add_limit_order(self, side, price, quantity):
        order = Order(
            id = next(self.order_ids),
            side = side,
            order_type = 'limit',
            price = price,
            quantity = quantity
        )

        print (f"\nNEW ORDER: {order}")

        if side == 'buy':
            self.match_buy(order)
            if order.quantity > 0:
                self.buys.append(order)
        
        elif side == 'sell':
            self.match_sell(order)
            if order.quantity > 0:
                self.sells.append(order)
        else:
            print('Invalid side. Use "buy" or "sell"')

        self.sort_book()
        return order.id
    
    def add_market_order(self, side, quantity):
        order = Order(
            id = next(self.order_ids),
            side = side,
            order_type = 'market',
            quantity = quantity
        )

        print (f"\nNEW ORDER: {order}")

        if side == 'buy':
            self.match_buy(order, is_market = True)

        elif side == 'sell':
            self.match_sell(order, is_market = True)
        else:
            print('Invalid side. Use "buy" or "sell"')
            return None
            
        return order.id
    
    def match_buy(self, buy_order, is_market = False):
        self.sort_book()
        
        while buy_order.quantity > 0. and self.sells:
            best_sell = self.sells[0]

            if not is_market and buy_order.price < best_sell.price:
                break

            trade_quantity = min(buy_order.quantity, best_sell.quantity)
            trade_price = best_sell.price

            trade = Trade(
                buy_order_id = buy_order.id, 
                sell_order_id = best_sell.id, 
                quantity = trade_quantity, 
                price = trade_price,     
            )

            self.trades.append(trade)
            print(trade)

            self.price_history.append(trade_price)

            buy_order.quantity -= trade_quantity 
            best_sell.quantity -= trade_quantity 

            if best_sell.quantity == 0:
                self.sells.pop(0)

    def match_sell(self, sell_order, is_market = False):
        self.sort_book()

        while sell_order.quantity > 0. and self.buys:
            best_buy = self.buys[0]

            if not is_market and sell_order.price > best_buy.price:
                break

            trade_quantity = min(sell_order.quantity, best_buy.quantity)
            trade_price = best_buy.price

            trade = Trade(
                buy_order_id = best_buy.id, 
                sell_order_id = sell_order.id, 
                quantity = trade_quantity, 
                price = trade_price,     
            )

            self.trades.append(trade)
            print(trade)

            sell_order.quantity -= trade_quantity 
            best_buy.quantity -= trade_quantity 

            if best_buy.quantity == 0:
                self.buys.pop(0)

    def cancel_order(self, order_id):
        for order in self.buys:
            if order.id == order_id:
                self.buys.remove(order)
                print(f"Cancelled order: #{order_id}")
                return 
        for order in self.sells:
            if order.id == order_id:
                self.sells.remove(order)
                print(f'Cancelled order: #{order_id}')
                return 
            
        print(f"Order #{order_id} not found.")

    def sort_book(self):
        self.buys.sort(key = lambda order: order.price, reverse = True)
        self.sells.sort(key = lambda order: order.price)

    def best_bid(self):
        if not self.buys:
            return None
        return self.buys[0].price
    
    def best_ask(self):
        if not self.sells:
            return None
        return self.sells[0].price
    
    def spread(self):
        if self.best_bid() is None or self.best_ask() is None:
            return None
        return self.best_ask() - self.best_bid()
    def show_book(self):
        self.sort_book()

        print("\n ======== ORDER BOOK =======")

        print("\nSELLS:")

        if not self.sells:
            print('None')
        else:
            for order in self.sells:
                print(order)

        print("\n BEST BID:", self.best_bid())
        print("BEST ASK:", self.best_ask())
        print('SPREAD:', self.spread())

        print("====================================")

    def show_trades(self):
        print("\n ======== TRADE HISTORY =======")

        if not self.trades:
                print("No trades exccuted yet")

        else:
            for trade in self.trades:
                    print(trade)

        print("====================================")

    def plot_price_history(self):
        if not self.price_history:
            print("No trades to plot yet.")
            return

        plt.plot(self.price_history, marker="o")
        plt.title("Simulated Trade Prices Over Time")
        plt.xlabel("Trade Number")
        plt.ylabel("Price")
        plt.show()

def run_demo():
    book = OrderBook()

    id1 = book.add_limit_order('buy', price = 100, quantity = 10)
    id2 = book.add_limit_order('sell', price = 101, quantity = 11)
    id3 = book.add_limit_order('buy', price = 99, quantity = 5)
    id4 = book.add_limit_order('sell', price = 10, quantity = 3)

    book.show_book()
    book.add_limit_order('buy', price = 101, quantity = 4)
    book.show_book()
    book.add_limit_order('sell', price = 100, quantity = 6)
    book.show_book()    
    book.add_market_order('buy', quantity = 5)
    book.show_book()
    book.cancel_order(142)
    book.show_book()
    book.show_trades()

    book.plot_price_history()

if __name__ == "__main__":
    run_demo()    
