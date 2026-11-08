# Crepto_market_analysis_btc
Btc_bot
Crypto Market Analysis Bot

A Python-based cryptocurrency market analysis bot that monitors market data from Gate.io and generates trading signals using technical indicators.

Features

- Fetches cryptocurrency market data from Gate.io public API.
- Analyzes closed candlesticks.
- Calculates technical indicators:
  - RSI
  - EMA
  - MACD
  - Moving Averages
  - Bollinger Bands
  - Stochastic Oscillator
  - Pivot Points
  - Support and Resistance levels
- Generates BUY and SELL signals based on technical analysis.
- Prevents repeated BUY or SELL signals.
- Optional Telegram notifications.
- Supports multiple timeframes.
- Displays market analysis in the terminal.

Technologies Used

- Python
- Pandas
- NumPy
- Requests
- Gate.io API
- Telegram Bot API (optional)

Installation

Install the required libraries:

pip install requests pandas numpy

Configuration

Telegram notifications are optional.

Set your Telegram credentials using environment variables:

export TELEGRAM_TOKEN="YOUR_BOT_TOKEN"
export TELEGRAM_CHAT_ID="YOUR_CHAT_ID"

Never publish your private Telegram token.

Run the Bot

python crypto_market_analysis_bot.py

Disclaimer

This project is for educational and research purposes only.

It provides market analysis and trading signals. It does not execute trades or guarantee profits.

Always test strategies and manage risk before making financial decisions.

Author

Developed as a personal Python project to practice financial market analysis, technical indicators, and API integration.
