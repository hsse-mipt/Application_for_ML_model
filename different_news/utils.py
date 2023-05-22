import feedparser
import pandas as pd
from sqlite3 import connect


class ParserRSS:
    def __init__(self, sources=None):
        self.sources = {
            'Kommersant': 'https://www.kommersant.ru/RSS/news.xml',
            'Lenta': 'https://lenta.ru/rss/',
            'Vesti': 'https://www.vesti.ru/vesti.rss',
            'RBC': 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss',
        } if sources is None else sources
        self.headlines = []
        self.descriptions = []
        self.links = []
        self.dates = []
        self.news_params = [['title', self.headlines],
                            ['description', self.descriptions],
                            ['link', self.links],
                            ['published', self.dates]]

    def add_source(self, source_name, source_link):
        self.sources[source_name] = source_link

    def __get_list_of_news_params(self):
        for _, rss_url in self.sources.items():
            feed = feedparser.parse(rss_url)
            for param_name, storage in self.news_params:
                storage.extend([news_item[param_name] for news_item in feed['items']])

    def get_all_news(self):
        self.__get_list_of_news_params()

        df = pd.DataFrame({
            'title': self.headlines,
            'description': self.descriptions,
            'link': self.links,
            'published': self.dates
        })

        df.to_sql(name='different_news_news',
                  con=connect('db.sqlite3'),
                  index=False,
                  if_exists='append')


def update_news():
    parser_ = ParserRSS()
    parser_.get_all_news()


if __name__ == '__main__':
    pass
