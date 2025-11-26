"use client";
import { useState } from "react";
import OrderForm from "./components/OrderForm";
import ResponseBox from "./components/ResponseBox";

export default function Home() {
  const [response, setResponse] = useState("");

  const submitOrder = async (order: any) => {
    const res = await fetch("/api/trade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(order),
    });

    const text = await res.text();
    setResponse(text);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-lg bg-gray-800 rounded-xl shadow-xl p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Trading Bot UI
        </h1>

        <OrderForm onSubmit={submitOrder} response={response} />

        <ResponseBox response={response} />
      </div>
    </div>
  );
}
