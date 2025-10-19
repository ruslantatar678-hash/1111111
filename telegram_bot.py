import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from fastapi import FastAPI
import logging

# ✅ Настройки
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "https://ruslantatar678-hash.onrender.com")  # <-- добавь сюда свой Render URL

# Если API_URL не найден — логируем предупреждение
if not API_URL or "http" not in API_URL:
    logging.warning(f"⚠️ API_URL не задан! Использую пример: https://ruslantatar678-hash.onrender.com")
    API_URL = "https://ruslantatar678-hash.onrender.com"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

app = FastAPI(title="Trading AI", description="AI-анализ валют и крипто. Сигналы по кнопке.", version="1.0")


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    print("❌ Webhook удалён")

@app.post(WEBHOOK_PATH)
async def process_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)
    return {"ok": True}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🤖 Бот подключён и готов к работе!")



