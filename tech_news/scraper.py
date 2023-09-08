import time
import requests
from parsel import Selector
import re
from tech_news.database import create_news
from time import sleep


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}

    time.sleep(1)

    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)

    news_links = selector.css(".entry-title a::attr(href)").getall()

    return news_links if news_links else []


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    next_page_url = selector.css("a.next::attr(href)").extract_first()

    return next_page_url


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)

    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css(".entry-details ~ .entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author > a::text").get()
    reading_time_text = selector.css(".meta-reading-time::text").get()
    reading_time = int(re.sub("[^0-9]", "", reading_time_text))
    summary = "".join(
        selector.css(".entry-content > p:first-of-type *::text").getall()
    ).strip()
    category = selector.css(".category-style .label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(n):
    all_news = []
    url = "https://blog.betrybe.com"

    while len(all_news) < n:
        html_content = fetch(url)
        news_links = scrape_updates(html_content)

        for link in news_links:
            news_content = fetch(link)
            news_details = scrape_news(news_content)
            all_news.append(news_details)

            if len(all_news) >= n:
                break

        next_page_link = scrape_next_page_link(html_content)

        if next_page_link is None:
            break

        url = next_page_link
        sleep(1)

    create_news(all_news)
    return all_news[:n]
