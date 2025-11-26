from fastapi import FastAPI
from pydantic import BaseModel
from basic_bot import BasicBot
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = BasicBot()
class Order(BaseModel):
    symbol: str
    side: str
    qty: float
    type: str
    price: float | None = None
    stop_price: float | None = None
    limit_price: float | None = None

def format_order(order, label=None):
    return {
        "label": label,
        "orderId": order.get("orderId"),
        "symbol": order.get("symbol"),
        "type": order.get("type"),
        "status": order.get("status"),
        "price": order.get("price"),
        "stopPrice": order.get("stopPrice"),
        "avgPrice": order.get("avgPrice"),
        "qty": order.get("origQty"),
        "executedQty": order.get("executedQty"),
        "updateTime": order.get("updateTime")
    }
@app.post("/order")
def create_order(order: Order):
    try:
        order_type = order.type.lower()

        if order_type == "market":
            result = bot.market_order(
                order.symbol.upper(),
                order.side.upper(),
                order.qty
            )
            return {
                "success": True,
                "type": "market",
                "summary": {
                    "symbol": order.symbol.upper(),
                    "side": order.side.upper(),
                    "qty": order.qty
                },
                "orders": [
                    format_order(result, label="Execution")
                ]
            }

        elif order_type == "limit":
            if order.price is None:
                return {"success": False, "error": "Limit order requires price"}

            result = bot.limit_order(
                order.symbol.upper(),
                order.side.upper(),
                order.qty,
                order.price
            )

            return {
                "success": True,
                "type": "limit",
                "summary": {
                    "symbol": order.symbol.upper(),
                    "side": order.side.upper(),
                    "qty": order.qty,
                    "price": order.price
                },
                "orders": [
                    format_order(result, label="Limit Order")
                ]
            }

        elif order_type == "oco":
            if order.stop_price is None or order.limit_price is None:
                return {
                    "success": False,
                    "error": "stop_price and limit_price required for OCO"
                }

            result = bot.oco_order(
                order.symbol.upper(),
                order.side.upper(),
                order.qty,
                order.stop_price,
                order.limit_price
            )

            return {
                "success": True,
                "type": "oco",
                "summary": {
                    "symbol": order.symbol.upper(),
                    "side": order.side.upper(),
                    "qty": order.qty
                },
                "orders": [
                    format_order(result["stop_order"], label="Stop Loss"),
                    format_order(result["limit_order"], label="Take Profit")
                ]
            }

        else:
            return {"success": False, "error": "Invalid order type"}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/prices")
def get_prices():
    try:
        tickers = bot.client.futures_ticker()
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT"]

        data = [
            {"symbol": t["symbol"], "price": float(t["lastPrice"])}
            for t in tickers
            if t["symbol"] in symbols
        ]

        return {"success": True, "data": data}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
