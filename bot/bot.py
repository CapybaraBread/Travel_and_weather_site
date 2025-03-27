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
    "Москва": (55.7558, 37.6173),
    "Санкт-Петербург": (59.9343, 30.3351),
    "Новосибирск": (55.0084, 82.9357),
    "Екатеринбург": (56.8389, 60.6057),
    "Казань": (55.7963, 49.1088),
    "Челябинск": (55.1644, 61.4368),
    "Омск": (54.9885, 73.3242),
    "Ростов-на-Дону": (47.2225, 39.7188),
    "Воронеж": (51.6755, 39.2089),
    "Смоленск": (54.7826, 32.0453),
    "Кострома": (57.8029, 40.9900)
}


async def start(update: Update, context):
    keyboard = [[city] for city in CITIES]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_text = (
        "👋 Приветствую тебя, искатель прогноза!\n"
        "Я — бот-метеоролог, готовый рассказать тебе о погоде в городах России.\n\n"
        "Выбери город ниже, чтобы получить актуальную информацию о погоде."
    )
    await update.message.reply_text(welcome_text, reply_markup=markup)


async def send_weather(update: Update, context):
    city = update.message.text
    if city in CITIES:
        lat, lon = CITIES[city]
        url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
        headers = {"X-Yandex-Weather-Key": YANDEX_WEATHER_TOKEN}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            weather_data = response.json()
            file_name = "weather.json"
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(weather_data, file, ensure_ascii=False, indent=4)

            await update.message.reply_text(
                f"🌤 Погода для {city} получена и сохранена.\n"
                "Смотри подробности здесь: https://msk.durka.keenetic.pro/website/"
            )
        else:
            await update.message.reply_text("❌ Ошибка при получении данных о погоде.")
    else:
        await update.message.reply_text("Пожалуйста, выбери город из списка кнопок 👇")


def main():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_weather))
    app.run_polling()


if __name__ == "__main__":
    main()
