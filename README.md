How to Run the Project

Backend (FastAPI)
cd traiding_bot_backend pip install -r requirements.txt uvicorn server:app --reload --port 8000

Backend runs at: http://localhost:8000

Environment Variables
Create a .env file inside traiding_bot_backend/:

BINANCE_API_KEY=your_key BINANCE_SECRET_KEY=your_secret

Frontend (Next.js)
npm install npm run dev

Frontend runs at: http://localhost:3000

CLI Usage
cd traiding_bot_backend python cli.py

Lets you place Market/Limit orders through the terminal.
