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
- Buy price ≥ Sell price
- Market orders execute immediately at best available price
