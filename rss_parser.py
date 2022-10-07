"""
Модуль по сбору новостей из RSS
Модуль обеспечивает подключение rss-каналов
Масштабирование за счет добавление новых ролей с указанием тематических каналов.
"""

# TODO описать функционал
# TODO сделать кодревью
# TODO добавить выгрузку за врменной период


import feedparser
import pandas as pd
from dateutil import parser

PATH_PROJECT = ""
DATASET_PATH = PATH_PROJECT + "dataset/"
RSS_FILENAME = DATASET_PATH + "rss_dataset.csv"


class ParseRSS():
    # заголовок
    def __init__(self, roles_rss_feeds):
        self.roles_rss_feeds = roles_rss_feeds

    def parse_feeds(self):
        roles = []
        titles = []
        tags = []
        summary = []
        descriptions = []
        links = []
        published_dt = []

        for role_name, rss_feeds in self.roles_rss_feeds.items():
            print(role_name)
            for url in rss_feeds:
                print(url)
                lenta = feedparser.parse(url)
                for item_news in lenta['items']:
                    roles.append(role_name)
                    titles.append(item_news['title'])
                    tags.append(" ".join([x["term"] for x in item_news['tags']]))
                    summary.append(item_news['summary'])
                    descriptions.append(item_news['description'])
                    links.append(item_news['link'])
                    published_dt.append(parser.parse(item_news['published']))
        feeds = {"news_for_role": roles, "title": titles, "tags": tags, "summary": summary, "description": descriptions,
                 "link": links,
                 "published_dt": published_dt}
        return feeds

    def dataset_to_csv(self, feeds):
        """Формирует csv файл в формате Pandas с полями:
        'news_for_role' - поле отражающее для какой роли были собраны новости
        'title', 'tags', 'summary', 'description', 'link', 'published_dt' - атрибуты rss ленты
        """
        df = pd.DataFrame.from_dict(feeds)
        df.to_csv(RSS_FILENAME, sep=";", encoding="utf-8-sig", header=True, index=True)
        return RSS_FILENAME


if __name__ == "__main__":
    roles_rss_feeds = {"booker": ['https://lenta.ru/rss/', 'http://www.consultant.ru/law/rss/'],
                       "owner": ['https://www.kommersant.ru/RSS/news.xml', 'https://www.vesti.ru/vesti.rss']}
    rss = ParseRSS(roles_rss_feeds)
    feeds = rss.parse_feeds()
    rss.dataset_to_csv(feeds)
