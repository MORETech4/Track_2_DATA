import json

# TODO актуализировать список rss каналов

# Сущность Роль, характеристики ролей, интересующие каналы
config = {}
config['ROLES_FEEDS'] = \
    {
        "booker": {
            "feeds": [
                'http://www.consultant.ru/rss/db.xml',
                'http://www.consultant.ru/rss/hotdocs.xml',  # нет tags summary summary_detail
                "https://glavkniga.ru/rss/yandexnews",
                "https://minjust.gov.ru/ru/subscription/rss/events/",
            ],
            "info": ["налог", "контролирующие органы", "МСФО", "юрлиц", "физлиц", "инспекция", "налоговик",
                     "налогоплательщик", "налоговый учет", "баланс", "бюджетирование", "ИФНС", "ПФР", "ФСС", "ФОТ", ]
        },
        "owner": {
            "feeds": [
                "https://minjust.gov.ru/ru/subscription/rss/events/"
                'https://www.kommersant.ru/RSS/news.xml', 'https://www.vesti.ru/vesti.rss'
            ],
            "info": ["минпромторг", ]
        }
    }

# Пути
config['PATH_PROJECT'] = ''
config['DATASET_PATH'] = config['PATH_PROJECT'] + "dataset/"
config['RSS_FILENAME'] = config['DATASET_PATH'] + "rss_dataset.csv"
config['LENTA_DATASET_PATH'] = config['DATASET_PATH'] + "src_rss_archive/"  # архивные данные по ленте
config['LENTA_ARCHIVE_RSS'] = config['LENTA_DATASET_PATH'] + "clear_mini_lenta_ru_news.csv"  # архивные данные по ленте

with open('config.json', 'w') as f:
    json.dump(config, f, indent=4)
