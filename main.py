from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import threading
import time

from app.ai_logic import analyze_pair

app = FastAPI(title="Trading AI", description="AI-анализ валют и крипто. Сигналы по кнопке.", version="1.0")

MANUAL_TRIGGER_TOKEN = os.getenv("MANUAL_TRIGGER_TOKEN", "demo-token")
ACTIVE_TRADES = {}

class SignalRequest(BaseModel):
    pair: str
    timeframe: str
    comment: str | None = None

def close_trade_after_timeout(trade_id: str, timeout: int = 120):
    time.sleep(timeout)
    if trade_id in ACTIVE_TRADES:
        ACTIVE_TRADES[trade_id]["status"] = "closed"
        ACTIVE_TRADES[trade_id]["closed_at"] = datetime.utcnow().isoformat()

@app.get("/healthz")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/trigger-signal")
def trigger_signal(req: SignalRequest, authorization: str | None = Header(None)):
    if authorization is None or authorization.split()[-1] != MANUAL_TRIGGER_TOKEN:
        raise HTTPException(status_code=401, detail="Неавторизован")

    analysis = analyze_pair(req.pair, req.timeframe)

    trade_id = f"{req.pair}_{int(datetime.utcnow().timestamp())}"
    ACTIVE_TRADES[trade_id] = {
        "pair": req.pair,
        "timeframe": req.timeframe,
        "comment": req.comment,
        "status": "active",
        "opened_at": datetime.utcnow().isoformat(),
        "expires_in_sec": 120,
        "ai_analysis": analysis,
    }

    threading.Thread(target=close_trade_after_timeout, args=(trade_id,), daemon=True).start()

    return {
        "ok": True,
        "message": "Сигнал создан. Сделка активна 2 минуты.",
        "trade_id": trade_id,
        "analysis": analysis
    }

@app.get("/trades")
def get_trades():
    return {"trades": ACTIVE_TRADES}
