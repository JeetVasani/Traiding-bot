import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const backendRes = await fetch("http://localhost:8000/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const text = await backendRes.text();   // read raw output
    console.log("RAW BACKEND RESPONSE:", text);

    // Try to parse JSON safely
    try {
      return NextResponse.json(JSON.parse(text));
    } catch {
      return NextResponse.json({ error: "Invalid JSON from backend", raw: text });
    }

  } catch (err: any) {
    return NextResponse.json({
      error: "Could not reach backend",
      details: String(err)
    });
  }
}


