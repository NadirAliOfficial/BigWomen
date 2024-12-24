# IBKR Telegram Trading Bot

This is a Telegram bot that allows you to place buy and sell orders on Interactive Brokers (IBKR) via the TWS API. The bot takes commands such as "buy" or "sell," then asks for the stock symbol and percentage of portfolio value to invest in the selected stock. The bot will calculate the number of shares to buy or sell based on the percentage and place the order using IBKR’s API.

## Features
- **Buy & Sell**: Place buy or sell orders based on portfolio value and the percentage you provide.
- **Portfolio-based Trading**: The bot calculates how much of your portfolio to invest in a specific stock based on the percentage you enter.
- **Telegram Integration**: Manage orders via a simple Telegram interface.
- **Interactive Workflow**: The bot asks for the stock symbol and percentage before executing the trade.

## Prerequisites

Before you begin, make sure you have the following:

- **Interactive Brokers (IBKR) account** with TWS (Trader Workstation) running.
- **Telegram Bot API Token**: Create a bot on Telegram and get your bot token by talking to [BotFather](https://core.telegram.org/bots#botfather).
- **Python 3.x**: Make sure Python is installed on your machine.
- **Required Libraries**: You'll need to install some Python libraries.

## Installation

### 1. Install Dependencies

Clone this repository and install the required libraries:

```bash
git clone <repository-url>
cd <repository-folder>
pip install -r requirements.txt
```

### 2. Install Interactive Brokers API (IB-insync)

To interact with the IBKR API, you need the **IB-insync** library. Install it using pip:

```bash
pip install ib_insync
```

### 3. Set Up Your Telegram Bot

Create a bot on Telegram by chatting with [BotFather](https://core.telegram.org/bots#botfather) and get your **API token**.

### 4. Configure the Bot Token

In the code, update the following line with your **Telegram bot API token**:

```python
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
```

### 5. Set Up Interactive Brokers TWS

Ensure that **TWS** is installed and running on your machine. The bot will connect to the TWS using the default port (7497).

## Usage

### 1. Start the Bot

Run the bot using the following command:

```bash
python telegram_trading_bot.py
```

Once the bot is running, you can interact with it via Telegram.

### 2. Interaction Flow

1. **Send `/buy` or `/sell`** to start the process.
2. **Bot will ask for a stock symbol** (e.g., `AAPL`).
3. **Bot will then ask for the percentage** of your portfolio to invest in the selected stock (e.g., `5%`).
4. The bot will **calculate the number of shares** based on your portfolio value and place a **market order** to buy or sell the stock.

### Example Interaction:

- **User sends**: `/buy`
- **Bot responds**: "What action would you like to perform? (buy/sell)"
- **User sends**: `buy`
- **Bot responds**: "Please enter the stock symbol (e.g., AAPL)."
- **User sends**: `AAPL`
- **Bot responds**: "Please enter the percentage you want to invest in AAPL (e.g., 5%)."
- **User sends**: `5%`
- **Bot responds**: "Buying X shares of AAPL."

### 3. Cancel the Operation

If you want to cancel the operation at any time, just send `/cancel`.

### 4. Portfolio Value Calculation

The bot calculates the percentage of your portfolio that you wish to invest in based on the **current value** of your holdings. The stock price is fetched in real-time, and the number of shares is calculated using the formula:

```
shares_to_buy = (portfolio_value * percentage) / stock_price
```

### 5. Order Execution

Once the percentage and symbol are provided, the bot calculates how many shares to buy or sell and places a **market order** through IBKR using the TWS API.

## Configuration

You can configure the bot’s parameters:

- **TWS Host and Port**: By default, the bot connects to `127.0.0.1:7497`. If your TWS is running on a different machine or port, update this in the code:

```python
ib.connect('127.0.0.1', 7497, clientId=1)
```

- **Telegram API Token**: Update your bot’s token:

```python
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
```

## Error Handling

- The bot ensures that the **percentage** is between 1% and 100%.
- If the input is invalid, the bot will prompt the user to enter a valid value.
- If the **market data** for the stock is unavailable, the bot will notify the user and not place the order.

## License

This project is licensed under the MIT License.
## Troubleshooting

- **TWS API not responding**: Make sure that TWS is running and the API is enabled. Check the TWS logs for any connection errors.
- **Invalid Telegram token**: Ensure you have entered the correct bot token from BotFather.
