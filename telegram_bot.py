import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from fastapi import FastAPI

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "https://ruslantatar678-hash.onrender.com")

# Удаляем лишний слэш на конце, если вдруг есть
if API_URL.endswith("/"):
    API_URL = API_URL[:-1]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{API_URL}{WEBHOOK_PATH}"

app = FastAPI()

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



