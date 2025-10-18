FROM python:3.11-slim

WORKDIR /app

# Чтобы Python видел модуль "app"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# ✅ Запускаем FastAPI и Telegram-бота
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python app/telegram_bot.py"]
