import requests
from django.shortcuts import render
import json
from bs4 import BeautifulSoup


def show_pages(request):
    events = []
    python_page = requests.get("https://experience.tripster.ru/experience/Moscow/?page=2")
    soup = BeautifulSoup(python_page.text, 'html.parser')
    event_titles = soup.find_all(class_="title")
    event_text = soup.find_all(class_="tagline")
    event_img_urls = soup.find_all(class_="exp-pic lazy-image")
    event_prices = soup.find_all(class_="price-current")
    event_reviews = soup.find_all(class_='reviews')
    event_rating = soup.find_all(class_='rating-value')
    for i in range(0, len(event_titles)):
        events.append({
            'title': event_titles[i].get_text(),
            'text': event_text[i].get_text(),
            'price': event_prices[i].get_text(),
            'img_url': event_img_urls[i].get('src'),
            'reviews': event_reviews[i].get_text(),
            'rating': event_rating[i].get_text(),
        })
    with open("Towns.json", "w", encoding='utf8') as write_file:
        json.dump(events, write_file, indent=4, ensure_ascii=False)
    return render(request, 'main/towns.html', context=events)

