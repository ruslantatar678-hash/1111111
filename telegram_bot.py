import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("MANUAL_TRIGGER_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

FOREX_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF",
               "NZD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY", "EUR/CHF"]
CRYPTO_PAIRS = ["BTC/USD", "ETH/USD", "BNB/USD", "XRP/USD", "SOL/USD",
                "DOGE/USD", "ADA/USD", "AVAX/USD", "LINK/USD", "MATIC/USD"]
TIMEFRAME = "1m"

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💱 Валютные пары", "💰 Крипто пары")
    await message.answer("Привет! Выбери тип актива:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "💱 Валютные пары")
async def choose_forex(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for pair in FOREX_PAIRS:
        keyboard.add(types.InlineKeyboardButton(pair, callback_data=f"pair:{pair}"))
    await message.answer("Выбери валютную пару:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "💰 Крипто пары")
async def choose_crypto(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for pair in CRYPTO_PAIRS:
        keyboard.add(types.InlineKeyboardButton(pair, callback_data=f"pair:{pair}"))
    await message.answer("Выбери крипто пару:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("pair:"))
async def handle_pair(callback: types.CallbackQuery):
    pair = callback.data.split("pair:")[1]
    confirm_kb = types.InlineKeyboardMarkup()
    confirm_kb.add(
        types.InlineKeyboardButton("🚀 Отправить сигнал", callback_data=f"send:{pair}"),
        types.InlineKeyboardButton("↩️ Назад", callback_data="back")
    )
    await callback.message.edit_text(f"Пара: {pair}\nОтправить сигнал?", reply_markup=confirm_kb)

@dp.callback_query_handler(lambda c: c.data.startswith("send:"))
async def send_signal(callback: types.CallbackQuery):
    pair = callback.data.split("send:")[1]
    payload = {"pair": pair, "timeframe": TIMEFRAME}
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(f"{API_URL}/trigger-signal", json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            msg = f"✅ Сигнал отправлен!\nПара: {pair}\n⏱ Сделка активна 2 минуты\n📊 {data['analysis']['summary']}"
        else:
            msg = f"⚠️ Ошибка: {res.text}"
    except Exception as e:
        msg = f"🚫 Не удалось подключиться к API: {e}"

    await callback.message.edit_text(msg)

@dp.callback_query_handler(lambda c: c.data == "back")
async def go_back(callback: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💱 Валютные пары", "💰 Крипто пары")
    await callback.message.answer("Выбери тип актива:", reply_markup=keyboard)

def start_bot():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    from aiogram.utils.executor import start_webhook
    import os

    API_URL = os.getenv("API_URL", "https://<имя_твоего_сервиса>.onrender.com")
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    WEBHOOK_PATH = f"/webhook/{TOKEN}"
    WEBHOOK_URL = f"{API_URL}{WEBHOOK_PATH}"

    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")

    async def on_shutdown(dp):
        await bot.delete_webhook()
        print("🛑 Webhook удалён")

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=8000,
    )

