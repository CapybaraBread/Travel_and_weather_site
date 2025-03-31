import requests
from django.shortcuts import render
import json
from bs4 import BeautifulSoup


def show_pages(request, page=1):
    with open("weather.json", "r", encoding="utf8") as json_file:
        json_file = json.load(json_file)
        weather = json_file["forecast"]
        town = json_file["name"]
    towns = {
        "Москва": "Moscow",
        "Санкт-Петербург": "Saint_Petersburg",
        "Новосибирск": "Novosibirsk",
        "Екатеринбург": "Yekaterinburg",
        "Казань": "Kazan",
        "Челябинск": "Chelyabinsk",
        "Омск": "Omsk",
        "Ростов-на-Дону": "Rostov-on-Don",
        "Воронеж": "Voronezh",
        "Смоленск": "Smolensk",
        "Кострома": "Kostroma"
    }
    url = f"https://experience.tripster.ru/experience/{towns[town]}/"
    town_name = {
        "name": town
    }
    events = []
    params = {
        'page': page
    }
    python_page = requests.get(url, params=params)
    soup = BeautifulSoup(python_page.text, 'html.parser')
    event_titles = soup.find_all(class_="title")
    event_text = soup.find_all(class_="tagline")
    event_img_urls = soup.find_all(class_="exp-pic lazy-image")
    event_prices = soup.find_all(class_="price-current")
    event_rating = soup.find_all(class_='rating-value')
    max_page = 0
    for pages in soup.find_all(class_="router-link-active item"):
        max_page = int(pages.get_text())
    for counter in range(0, len(event_titles)):
        try:
            events.append({
                'title': event_titles[counter].get_text(),
                'text': event_text[counter].get_text(),
                'img_url': event_img_urls[counter].get('src'),
                'price': event_prices[counter].get_text(),
                'rating': event_rating[counter].get_text(),
            })
        except IndexError:
            try:
                events.append({
                    'title': event_titles[counter].get_text(),
                    'text': event_text[counter].get_text(),
                    'img_url': event_img_urls[counter].get('src'),
                    'price': event_prices[counter].get_text(),
                    'rating': "Нет",
                })
            except IndexError:
                try:
                    events.append({
                        'title': event_titles[counter].get_text(),
                        'text': event_text[counter].get_text(),
                        'img_url': event_img_urls[counter].get('src'),
                        'price': "Нет",
                        'rating': event_rating[counter].get_text(),
                    })
                except IndexError:
                    events.append({
                        'title': event_titles[counter].get_text(),
                        'text': event_text[counter].get_text(),
                        'img_url': event_img_urls[counter].get('src'),
                        'price': "Нет",
                        'rating': "Нет",
                    })
    pages = {
        'next_page': int(page) + 1,
        'page': int(page),
        'prev_page': int(page) - 1,
        'max_page': max_page,
    }
    with open("Towns.json", "w", encoding='utf8') as write_file:
        json.dump(events, write_file, indent=4, ensure_ascii=False)
    with open("Towns.json", "r", encoding='utf8') as events_file:
        return render(request, 'index.html', context={
            'events': json.load(events_file),
            "pages": pages,
            "town": town_name,
            "weather": weather,
        })


