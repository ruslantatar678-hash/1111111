import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Trading AI",
    description="AI-анализ валют и крипто. Сигналы по кнопке.",
    version="1.0",
)

# Токен для ручного вызова сигналов
MANUAL_TRIGGER_TOKEN = os.getenv("MANUAL_TRIGGER_TOKEN", "demo-token")
ACTIVE_TRADES = {}

# 🔹 Проверка работы API
@app.get("/")
async def root():
    return {"message": "🚀 API работает! Всё в порядке."}

# 🔹 Обработчик сигналов от Telegram-бота
@app.post("/trigger-signal")
async def trigger_signal(request: Request):
    try:
        data = await request.json()
        token = data.get("token")
        pair = data.get("pair")
        signal = data.get("signal")

        if token != MANUAL_TRIGGER_TOKEN:
            return JSONResponse(status_code=403, content={"error": "Неверный токен доступа"})

        print(f"📊 Получен сигнал: {pair} → {signal}")
        ACTIVE_TRADES[pair] = signal

        return {"status": "ok", "message": f"Сигнал {signal} для {pair} принят"}

    except Exception as e:
        print("Ошибка при приёме сигнала:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

# 🔹 Проверка активных сигналов
@app.get("/active-trades")
async def active_trades():
    return ACTIVE_TRADES
