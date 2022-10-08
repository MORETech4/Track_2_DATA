"""
Модуль по сбору новостей из RSS
Модуль обеспечивает подключение rss-каналов
Масштабирование за счет добавление новых ролей с указанием тематических каналов.
"""

# TODO описать функции
# TODO сделать кодревью
# TODO добавить выгрузку за врменной период
# TODO уйти от необходмиости два раза указывать наименования колонок


import feedparser
import pandas as pd
from dateutil import parser
from datetime import datetime, timezone


PATH_PROJECT = ""
DATASET_PATH = PATH_PROJECT + "dataset/"
RSS_FILENAME = DATASET_PATH + "rss_dataset.csv"


class ParseRSS():
    # заголовок
    def __init__(self, roles_rss_feeds, is_log=True):
        self.roles_rss_feeds = roles_rss_feeds
        self.is_log = is_log

    def parse_feeds(self):
        roles = []
        titles = []
        tags = []
        summary = []
        descriptions = []
        links = []
        published_dt = []
        published_ts = []

        for role_name, rss_feeds in self.roles_rss_feeds.items():
            if self.is_log:
                print(role_name)
            for url in rss_feeds:
                if self.is_log:
                    print(url)
                lenta = feedparser.parse(url)
                for item_news in lenta['items']:
                    roles.append(role_name)
                    titles.append(item_news['title'])
                    print(item_news.keys())
                    if tags in list(item_news.keys()):
                        tags.append(" ".join([x["term"] for x in item_news['tags']]))
                    else:
                        tags.append("")
                    if 'summary' in item_news and item_news['summary'] != "":
                        summary.append(item_news['summary'])
                    else:
                        summary.append(item_news['title'])
                    if 'description' in item_news and item_news['description'] != "":
                        descriptions.append(item_news['description'])
                    else:
                        if 'summary' in item_news and item_news['summary'] != "":
                            descriptions.append(item_news['summary'])
                        else:
                            descriptions.append(item_news['title'])
                    links.append(item_news['link'])
                    if 'published' in item_news and item_news['published'] != "":
                        dt_publish = parser.parse(item_news['published'])
                    else:
                        dt_publish = datetime.now(timezone.utc).replace(microsecond=0)
                    # добавляем дату публикации
                    published_dt.append(dt_publish)
                    # Дату переводим в таймстеп
                    published_ts.append(dt_publish.timestamp())

        feeds = {"news_for_role": roles, "title": titles, "tags": tags, "summary": summary, "description": descriptions,
                 "link": links, "published_dt": published_dt, "published_ts": published_ts}
        return feeds

    def dataset_to_csv(self, feeds):
        """Формирует csv файл в формате Pandas с полями:
        'news_for_role' - поле отражающее для какой роли были собраны новости
        'title', 'tags', 'summary', 'description', 'link', 'published_dt' - атрибуты rss ленты
        """
        df = pd.DataFrame.from_dict(feeds)
        df.to_csv(RSS_FILENAME, sep=";", encoding="utf-8-sig", header=True, index=True, index_label="id")
        return RSS_FILENAME


if __name__ == "__main__":
    roles_rss_feeds = {
                        # "booker": ['http://www.consultant.ru/rss/db.xml', 'http://www.consultant.ru/law/rss/'],
                        "booker": [
                            'http://www.consultant.ru/rss/db.xml',
                            'http://www.consultant.ru/rss/hotdocs.xml', # нет tags summary summary_detail
                            "https://glavkniga.ru/rss/yandexnews",
                            "https://minjust.gov.ru/ru/subscription/rss/events/",
                        ],
                       "owner": [
                            "https://minjust.gov.ru/ru/subscription/rss/events/"
                            'https://www.kommersant.ru/RSS/news.xml', 'https://www.vesti.ru/vesti.rss']
    }
    rss = ParseRSS(roles_rss_feeds)
    feeds = rss.parse_feeds()
    rss.dataset_to_csv(feeds)
