from django.core.management.base import BaseCommand
from sqlite3 import connect

import feedparser
import csv

import pandas as pd
import re
from nltk.stem import SnowballStemmer


class ParserRSS:
    def __init__(self, sources=None, path='./news.csv'):
        self.sources = {
            'Kommersant': 'https://www.kommersant.ru/RSS/news.xml',
            'Lenta': 'https://lenta.ru/rss/',
            'Vesti': 'https://www.vesti.ru/vesti.rss',
            'RBC': 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss',
        } if sources is None else sources
        self.words = ''
        self.headlines = []
        self.descriptions = []
        self.links = []
        self.dates = []
        self.news_params = [['title', self.headlines],
                            ['description', self.descriptions],
                            ['link', self.links],
                            ['published', self.dates]]
        self.news_path = path
        self.stemmer = SnowballStemmer(language='russian')

    def add_source(self, source_name, source_link):
        self.sources[source_name] = source_link

    @staticmethod
    def __parse_elements(feed, news_parameter):
        storage = []
        for news_item in feed['items']:
            storage.append(news_item[news_parameter])
        return storage

    def __get_list_of_news_params(self):
        for _, rss_url in self.sources.items():
            feed = feedparser.parse(rss_url)
            for name, storage in self.news_params:
                storage.extend(self.__parse_elements(feed, name))

    def get_certain_news(self, all_news: pd.DataFrame, targets: list):
        for target in targets:
            target = self.stemmer.stem(target)

        results = []
        for target in targets:
            results.append(
                all_news.apply(
                    lambda x: x.str.contains(target,
                                             na=False,
                                             flags=re.IGNORECASE)).any(axis=1))

        sorted_news = all_news

        for res in results:
            sorted_news = all_news[sorted_news & res]

        sorted_news.to_csv(self.news_path, sep='\t', encoding='utf-8-sig')

        return sorted_news

    def get_all_news(self):
        self.__get_list_of_news_params()
        header = ['title', 'description', 'link', 'published']

        with open(self.news_path, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(elem for elem in header)

            for heading, news, link, date in zip(
                    self.headlines, self.descriptions, self.links, self.dates):
                writer.writerow((heading, news, link, date))

            data = pd.read_csv(self.news_path)

        return data


class Command(BaseCommand):
    help = "Единоразовый парсинг новостей для стартовой страницы"

    def handle(self, *args, **options):
        parser_ = ParserRSS()
        df = parser_.get_all_news()
        df.to_sql(name='different_news_news',
                  con=connect('db.sqlite3'),
                  index=False,
                  if_exists='append')
