import { NextResponse } from "next/server";

export async function GET() {
  try {
    const res = await fetch("http://localhost:8000/prices");
    const text = await res.text(); // read raw backend
    return NextResponse.json(JSON.parse(text));
  } catch (err) {
    return NextResponse.json({
      success: false,
      error: "Backend not responding",
      details: String(err),
    });
  }
}
