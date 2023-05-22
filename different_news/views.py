from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .forms import QueryForm

import pandas as pd
from sqlite3 import connect

cached = None


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
            global cached
            event = form.cleaned_data['event']
            entity = form.cleaned_data['entity']

            conn = connect('db.sqlite3')
            df = pd.read_sql('SELECT * FROM different_news_news', conn) if \
                cached is None else cached

            
            # filter_news = ParserRSS()
            # df = filter_news.get_certain_news(df, [event])

            titles = df['title']
            news = df['description']
            links = df['link']
            published = df['published']

            data = pd.DataFrame({
                'title': titles,
                'description': news,
                'link': links,
                'pub_date': published
            })

            data = data.head(3)

            with open('analyzed_news.json', 'w', encoding='utf-8-sig') as js_file:
                data.to_json(js_file, force_ascii=False)
        else:
            return HttpResponse('Invalid data')

        return render(request, self.template_name, context=self.context)
