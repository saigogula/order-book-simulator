Order Book Simulator

A Python-based trading engine that simulates a limit order book using price-time priority.

## Features
- Limit orders
- Market orders
- Matching engine
- Partial fills
- Order cancellation
- Best bid / best ask tracking
- Bid-ask spread calculation
- Trade history logging

## How It Works
Orders are matched when:
- **Buy orders** are sorted from highest price to lowest price
- **Sell orders** are sorted from lowest price to highest price

A trade happens when:

```text
buy price >= sell price
