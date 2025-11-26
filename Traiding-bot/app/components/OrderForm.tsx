"use client";
import { useState, useEffect } from "react";

export default function OrderForm({ onSubmit, response }: any) {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [side, setSide] = useState("BUY");
  const [qty, setQty] = useState<number | null>(0.002);
  const [price, setPrice] = useState<number | null>(null);
  const [type, setType] = useState("market");
  const [symbols, setSymbols] = useState<any[]>([]);
  const [stopPrice, setStopPrice] = useState<number | null>(null);
  const [limitPrice, setLimitPrice] = useState<number | null>(null);

  useEffect(() => {
    fetch("/api/prices")
      .then((res) => res.json())
      .then((data) => {
        console.log("PRICE DATA:", data);
        if (data.success) setSymbols(data.data);
      })
      .catch((err) => console.log("Error fetching prices:", err));
  }, []);

  const handleSubmit = () => {
    onSubmit({
      symbol,
      side,
      qty,
      price,
      type,
      stop_price: stopPrice,
      limit_price: limitPrice,
    });
  };

  return (
    <div className="space-y-4">

      {/* SYMBOL DROPDOWN */}
      <select
        className="w-full p-2 rounded bg-gray-700"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      >
        {symbols.map((item) => (
          <option key={item.symbol} value={item.symbol}>
            {item.symbol} – {item.price}
          </option>
        ))}
      </select>

      {/* SIDE */}
      <select
        className="w-full p-2 rounded bg-gray-700"
        value={side}
        onChange={(e) => setSide(e.target.value)}
      >
        <option>BUY</option>
        <option>SELL</option>
      </select>

      {/* QUANTITY */}
      <input
        type="number"
        className="w-full p-2 rounded bg-gray-700"
        placeholder="Quantity"
        value={qty === null ? "" : qty}
        onChange={(e) => {
          const v = e.target.value;
          setQty(v === "" ? null : parseFloat(v));
        }}
      />

      {/* ORDER TYPE */}
      <select
        className="w-full p-2 rounded bg-gray-700"
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        <option value="market">Market Order</option>
        <option value="limit">Limit Order</option>
        <option value="oco">OCO Order</option>
      </select>

      {/* LIMIT ORDER PRICE */}
      {type === "limit" && (
        <input
          type="number"
          className="w-full p-2 rounded bg-gray-700"
          placeholder="Limit Price"
          value={price === null ? "" : price}
          onChange={(e) => {
            const v = e.target.value;
            setPrice(v === "" ? null : parseFloat(v));
          }}
        />
      )}

      {/* OCO ORDER INPUTS */}
      {type === "oco" && (
        <>
          {/* STOP PRICE */}
          <input
            type="number"
            className="w-full p-2 rounded bg-gray-700"
            placeholder="Stop Price"
            value={stopPrice === null ? "" : stopPrice}
            onChange={(e) => {
              const v = e.target.value;
              setStopPrice(v === "" ? null : parseFloat(v));
            }}
          />

          {/* LIMIT PRICE */}
          <input
            type="number"
            className="w-full p-2 rounded bg-gray-700"
            placeholder="Take Profit Limit Price"
            value={limitPrice === null ? "" : limitPrice}
            onChange={(e) => {
              const v = e.target.value;
              setLimitPrice(v === "" ? null : parseFloat(v));
            }}
          />
        </>
      )}

      {/* SUBMIT BUTTON */}
      <button
        onClick={handleSubmit}
        className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded font-semibold"
      >
        Place Order
      </button>

    </div>
  );
}
