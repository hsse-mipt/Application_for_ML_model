from django.shortcuts import render
from .forms import QueryForm

from django.views import generic
################################
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
            results.append(all_news.apply(lambda x: x.str.contains(target,
                                                                   na=False,
                                                                   flags=re.IGNORECASE)).any(
                axis=1))

        sorted_news = all_news[results[0]]

        sorted_news.to_csv(self.news_path, sep='\t', encoding='utf-8-sig')

        return sorted_news

    def get_all_news(self):
        self.__get_list_of_news_params()
        header = ['Заголовок', 'Новость', 'Ссылка', 'Дата публикации']

        with open(self.news_path, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(elem for elem in header)

            for heading, news, link, date in zip(
                    self.headlines, self.descriptions, self.links, self.dates):
                writer.writerow((heading, news, link, date))

            data = pd.read_csv(self.news_path)

        return data


class IndexView(generic.ListView):
    form_class = QueryForm
    initial = {}
    template_name = "index.html"
    context_object_name = "latest_analyzed_news"
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        self.context['form'] = form
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.context['form'] = form

        if form.is_valid():
            event = form.cleaned_data['event']
            entity = form.cleaned_data['entity']

            p = ParserRSS()
            df = p.get_all_news()
            df = p.get_certain_news(df, [event])
            data = df.head(3)

            with open('analyzed_news.json', 'w', encoding='utf-8') as js_file:
                data.to_json(js_file, force_ascii=False)

        return render(request, self.template_name, context=self.context)
