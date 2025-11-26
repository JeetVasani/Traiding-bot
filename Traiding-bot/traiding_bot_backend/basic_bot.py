from binance.client import Client
from binance.enums import *
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BasicBot:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")

        if not api_key or not api_secret:
            raise Exception("API_KEY or API_SECRET missing in .env")

        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def validate(self, symbol, side, qty, price=None):
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")

        if qty <= 0:
            raise ValueError("Quantity must be > 0")

        if price is not None and price <= 0:
            raise ValueError("Price must be > 0")

    def market_order(self, symbol, side, qty):
        self.validate(symbol, side, qty)

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=qty
            )
            logging.info(f"Market Order: {order}")
            return order
        except Exception as e:
            logging.error(f"Market Order Error: {e}")
            raise

    def limit_order(self, symbol, side, qty, price):
        self.validate(symbol, side, qty, price)

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=qty,
                price=price
            )
            logging.info(f"Limit Order: {order}")
            return order
        except Exception as e:
            logging.error(f"Limit Order Error: {e}")
            raise

    def oco_order(self, symbol, side, qty, stop_price, limit_price):
        try:
            stop_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                stopPrice=stop_price,
                quantity=qty,
                timeInForce="GTC"
            )

            limit_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                price=limit_price,
                quantity=qty,
                timeInForce="GTC"
            )

            return {
                "success": True,
                "stop_order": stop_order,
                "limit_order": limit_order
            }

        except Exception as e:
            logging.error(f"OCO Order Error: {e}")
            raise
