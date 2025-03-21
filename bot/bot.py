import json
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
YANDEX_WEATHER_TOKEN = os.getenv("YANDEX_WEATHER_TOKEN")


CITIES = {
    "Москва": {"lat": 55.7558, "lon": 37.6173},
    "Санкт-Петербург": {"lat": 59.9343, "lon": 30.3351},
    "Новосибирск": {"lat": 55.0084, "lon": 82.9357},
    "Екатеринбург": {"lat": 56.8389, "lon": 60.6057},
    "Казань": {"lat": 55.7963, "lon": 49.1088},
    "Челябинск": {"lat": 55.1644, "lon": 61.4368},
    "Омск": {"lat": 54.9885, "lon": 73.3242},
    "Ростов-на-Дону": {"lat": 47.2225, "lon": 39.7188},
    "Воронеж": {"lat": 51.6755, "lon": 39.2089},
    "Смоленск": {"lat": 54.7826, "lon": 32.0453}
}


def get_keyboard():
    keyboard = [[city] for city in CITIES.keys()]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


async def start(update: Update, context):
    await update.message.reply_text("Выберите город для получения погоды:", reply_markup=get_keyboard())


async def send_weather(update: Update, context):
    city = update.message.text
    if city in CITIES:
        lat, lon = CITIES[city]["lat"], CITIES[city]["lon"]
        url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
        headers = {"X-Yandex-Weather-Key": YANDEX_WEATHER_TOKEN}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            weather_data = response.json()
            file_name = "weather_data.json"
            
            # Перезаписываем JSON
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(weather_data, file, ensure_ascii=False, indent=4)
            
            await update.message.reply_document(open(file_name, "rb"))
        else:
            await update.message.reply_text(f"Ошибка {response.status_code}: {response.text}")
    else:
        await update.message.reply_text("Выберите город из списка.")


def main():
    app = Application.builder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_weather))

    app.run_polling()

if __name__ == "__main__":
    main()