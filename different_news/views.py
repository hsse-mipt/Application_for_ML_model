from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .forms import QueryForm
from .utils import get_certain_news, find_first_ind

from text_tonality_analyze.views import get_prediction

from pandas import DataFrame


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

            df = get_certain_news(event.split())

            predictions = get_prediction(df['description'].to_numpy())

            negative = min(find_first_ind(predictions, -1), predictions.size - 1)
            neutral = min(find_first_ind(predictions, 0), predictions.size - 1)
            positive = min(find_first_ind(predictions, 1), predictions.size - 1)

            data = DataFrame({
                'title': [
                    df['title'].iloc[negative],
                    df['title'].iloc[neutral],
                    df['title'].iloc[positive],
                ],
                'description': [
                    df['description'].iloc[negative],
                    df['description'].iloc[neutral],
                    df['description'].iloc[positive],
                ],
                'link': [
                    df['link'].iloc[negative],
                    df['link'].iloc[neutral],
                    df['link'].iloc[positive],
                ],
                'pub_date': [
                    df['published'].iloc[negative],
                    df['published'].iloc[neutral],
                    df['published'].iloc[positive],
                ],
            })

            return HttpResponse(data.to_json(force_ascii=False))

        return HttpResponse('Invalid data')
