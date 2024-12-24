from ib_insync import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import math

# IBKR Setup
ib = IB()

# Connect to IBKR (ensure TWS is running and accessible)
ib.connect('127.0.0.1', 7497, clientId=1)

# Telegram Bot Setup
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_API_TOKEN'
updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# States for conversation handler
SYMBOL, PERCENTAGE = range(2)

# Function to get portfolio value
def get_portfolio_value():
    portfolio = ib.portfolio()
    return sum([p.position * p.marketPrice for p in portfolio])

# Function to calculate shares
def calculate_shares(symbol, percentage):
    portfolio_value = get_portfolio_value()
    stock_price = ib.reqMktData(Stock(symbol, 'SMART', 'USD'), '', False, False)
    ib.sleep(1)  # Allow time for the market data request to return
    stock_value = stock_price.last
    amount_to_invest = (percentage / 100) * portfolio_value
    shares = amount_to_invest / stock_value
    return math.floor(shares)  # Round to the nearest whole number

# Function to place a buy order
def buy_order(symbol, percentage):
    shares = calculate_shares(symbol, percentage)
    stock = Stock(symbol, 'SMART', 'USD')
    order = MarketOrder('BUY', shares)
    ib.placeOrder(stock, order)
    return f"Buying {shares} shares of {symbol}."

# Function to place a sell order
def sell_order(symbol, percentage):
    shares = calculate_shares(symbol, percentage)
    stock = Stock(symbol, 'SMART', 'USD')
    order = MarketOrder('SELL', shares)
    ib.placeOrder(stock, order)
    return f"Selling {shares} shares of {symbol}."

# Start command to begin conversation
def start(update: Update, context: CallbackContext):
    update.message.reply_text("What action would you like to perform? (buy/sell)")
    return SYMBOL

# Ask for stock symbol
def ask_symbol(update: Update, context: CallbackContext):
    action = update.message.text.lower()
    context.user_data['action'] = action
    update.message.reply_text("Please enter the stock symbol (e.g., AAPL).")
    return PERCENTAGE

# Ask for percentage
def ask_percentage(update: Update, context: CallbackContext):
    symbol = update.message.text.upper()
    context.user_data['symbol'] = symbol
    update.message.reply_text(f"Please enter the percentage you want to invest in {symbol} (e.g., 5%).")
    return ConversationHandler.END

# Process the command to buy or sell
def process_order(update: Update, context: CallbackContext):
    try:
        # Get symbol and percentage from user input
        symbol = context.user_data['symbol']
        percentage_str = update.message.text.strip()
        percentage = float(percentage_str.replace('%', ''))  # Remove '%' and convert to float

        if percentage <= 0 or percentage > 100:
            update.message.reply_text("Please provide a valid percentage (1-100).")
            return

        # Place the order
        if context.user_data['action'] == 'buy':
            result = buy_order(symbol, percentage)
        elif context.user_data['action'] == 'sell':
            result = sell_order(symbol, percentage)

        update.message.reply_text(result)

    except ValueError:
        update.message.reply_text("Invalid input. Please provide the percentage in the format '5%'.")

# Cancel conversation
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

# Set up the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('buy', start), CommandHandler('sell', start)],
    states={
        SYMBOL: [MessageHandler(Filters.text & ~Filters.command, ask_symbol)],
        PERCENTAGE: [MessageHandler(Filters.text & ~Filters.command, ask_percentage)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Add the conversation handler to the dispatcher
dispatcher.add_handler(conv_handler)

# Start the bot
updater.start_polling()
updater.idle()
