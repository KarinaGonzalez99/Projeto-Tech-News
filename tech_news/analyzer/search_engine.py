from tech_news.database import db
from datetime import datetime


# Requisito 7
def search_by_title(title):
    cursor = db.news.find({"title": {"$regex": f"(?i){title}"}})
    results = [(news["title"], news["url"]) for news in cursor]

    return results


# Requisito 8
def search_by_date(date):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    db_format_date = parsed_date.strftime("%d/%m/%Y")
    cursor = db.news.find({"timestamp": db_format_date})
    results = [(news["title"], news["url"]) for news in cursor]

    return results


# Requisito 9
def search_by_category(category):
    cursor = db.news.find({"category": {"$regex": f"(?i){category}"}})
    results = [(news["title"], news["url"]) for news in cursor]
    return results
