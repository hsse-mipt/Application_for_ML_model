import feedparser
from re import IGNORECASE
from nltk.stem import SnowballStemmer
from pandas import DataFrame

from .db_controller import read_data_from_db, write_data_to_db


class ParserRSS:
    stemmer = SnowballStemmer(language='russian')

    def __init__(self, sources=None):
        self.sources = {
            'Kommersant': 'https://www.kommersant.ru/RSS/news.xml',
            'Lenta': 'https://lenta.ru/rss/',
            'Vesti': 'https://www.vesti.ru/vesti.rss',
            'RBC': 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss',
            'Habr': 'https://habr.com/ru/rss/news/?fl=ru',
        } if sources is None else sources
        self.headlines = []
        self.descriptions = []
        self.links = []
        self.dates = []
        self.news_params = [['title', self.headlines],
                            ['description', self.descriptions],
                            ['link', self.links],
                            ['published', self.dates]]

    def add_source(self, source_name: str, source_link: str):
        self.sources[source_name] = source_link

    def __get_list_of_news_params(self):
        for _, rss_url in self.sources.items():
            feed = feedparser.parse(rss_url)
            for param_name, storage in self.news_params:
                storage.extend([news_item[param_name] for news_item in feed['items']])

    def get_all_news(self):
        self.__get_list_of_news_params()

        write_data_to_db(DataFrame({
            'title': self.headlines,
            'description': self.descriptions,
            'link': self.links,
            'published': self.dates
        }))


def update_news():
    parser_ = ParserRSS()
    parser_.get_all_news()


def get_certain_news(targets: list):
    all_news = read_data_from_db()

    for target in targets:
        target = ParserRSS.stemmer.stem(target)

    results = []
    for target in targets:
        results.append(
            all_news.apply(
                lambda x: x.astype(str).str.contains(target,
                                                     na=False,
                                                     flags=IGNORECASE)).any(axis=1))

    filter_mask = results[0]
    for res in results:
        filter_mask = filter_mask & res

    return all_news[filter_mask]


if __name__ == '__main__':
    pass
