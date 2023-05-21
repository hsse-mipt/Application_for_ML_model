import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from .forms import QueryForm

from django.views import generic


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

            # p = ParserRSS()
            df = pd.DataFrame()
            # df = p.get_certain_news(df, [event])
            # data = df.head(3)
            data = df

            for row in data.iterrows():
                pass

            with open('analyzed_news.json', 'w', encoding='utf-8-sig') as js_file:
                data.to_json(js_file, force_ascii=False)
        else:
            return HttpResponse('Invalid data')

        return render(request, self.template_name, context=self.context)
