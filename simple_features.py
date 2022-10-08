"""
Генератор простых признаков из данных (нумерные, категориальные, бинарные), простые обработчики текстов новостей
"""
# !pip install https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.1.0/ru_core_news_sm-3.1.0.tar.gz

# TODO сделать конфиг для хранения общих констант (есть переживания про проблемы с поиском путей, чтобы у всех все норм работало)
# TODO хорошо бы все обработчики объединить в один pipeline
# TODO удалять теги типа </ br>

PATH_PROJECT = ""
DATASET_PATH = PATH_PROJECT + "dataset/"
RSS_FILENAME = DATASET_PATH + "rss_dataset.csv"
SIMPLE_FEATURES_FILENAME = DATASET_PATH + "simple_f_dataset.csv"

import pandas as pd
import re

import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
rus_stopwords = stopwords.words("russian")
snowball = SnowballStemmer(language="russian")
nltk.download('punkt')

import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class TextProcessing():
    """
    Делаем следующую обрабатку текста:
    - downcase
    - лемматизация - боримся с окончаниями
    - убираем стоп-слова
    - стемминг - обрезаем окончания (опционально)
    """

    def __init__(self):
        pass

    def preprocessing_text(self, text):
        # приводим к нижнему регистру
        text = text.lower()
        # убираем стоп слова
        text = " ".join([w for w in re.findall(r"\w+", text) if w not in rus_stopwords])
        # лемматизация
        text = " ".join([morph.parse(w)[0].normal_form for w in text.split(' ')])
        # стемминг
        text = " ".join([snowball.stem(w) for w in text.split(' ')])
        return text

    def preprocessing_df(self, df, enable_stemming=False):
        self.df = df
        # Заполняем пустые значениям описания заголовком статьи
        self.fillna_columns()
        self.preprocessing_series(column="description", enable_stemming=enable_stemming)
        self.preprocessing_series(column="title", enable_stemming=enable_stemming)
        self.preprocessing_series(column="summary", enable_stemming=enable_stemming)
        return self.df

    def fillna_columns(self):
        df = self.df
        # Для случаев когда summary пустой заполняем title
        df["summary"] = df["summary"].fillna(df["title"])
        # Для случаев когда и title пустой использеум description
        df["summary"] = df["summary"].fillna(df["description"])
        df["description"] = df["description"].fillna(df["summary"])
        df["title"] = df["title"].fillna(df["summary"])

    def preprocessing_series(self, column, enable_stemming=False):
        # приводим к нижнему регистру
        self.df[f"{column}_preproc"] = self.lower_text(self.df[column])
        # убираем стоп слова
        self.df[f"{column}_preproc"] = self.stopwords(self.df[f"{column}_preproc"])
        # лемматизация
        self.df[f"{column}_preproc"] = self.lemmatization(self.df[f"{column}_preproc"])
        # стемминг
        if enable_stemming:
            self.df[f"{column}_preproc"] = self.stemming(self.df[f"{column}_preproc"])

    def lower_text(self, series):
        # приводим к нижнему регистру
        return series.str.lower()

    def stopwords(self, series):
        lemma_series = series.apply(lambda x: " ".join([w for w in re.findall(r"\w+", x) if w not in rus_stopwords]))
        return lemma_series

    def lemmatization(self, series):
        # лемматизация
        lemma_series = series.apply(lambda x: " ".join([morph.parse(w)[0].normal_form for w in x.split(' ')]))
        return lemma_series

    def stemming(self, series):
        # стемминг
        stemm_series = series.apply(lambda x: " ".join([snowball.stem(w) for w in x.split(' ')]))
        return stemm_series


# class SimpleFeatures():
#     def __init__(self, df):
#         self.df = df
#         self.calc_timestamp()
#
#     def calc_timestamp(self):
#         """
#         Дату переводим в таймстеп, чтобы у новостей был признак признак времени
#         Данный признак можно использовать для схожести новостей во времени,
#         поиске всплесков новостей во времени, продолжительность новостного
#         тренда и пр.
#         """



if __name__ == "__main__":
    news_df = pd.read_csv(RSS_FILENAME, sep=";", index_col=["id"])
    # ПредОбработка текста
    txt_proc = TextProcessing()
    news_df = txt_proc.preprocessing_df(news_df)

    news_df.to_csv(SIMPLE_FEATURES_FILENAME, sep=";", encoding="utf-8-sig", header=True, index=True, index_label="id")

    # # Получение простых признаков
    # simple_f = SimpleFeatures(news_df)
    # news_df = simple_f.df
    # print(news_df)
