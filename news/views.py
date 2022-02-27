from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse, Http404
from hypernews.settings import NEWS_JSON_PATH

import json
import datetime
import random


def get_news():
    with open(NEWS_JSON_PATH, 'r') as read_file:
        all_news = json.load(read_file)
    return all_news


class MainView(View):

    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):

    def get(self, request, *args, **kwargs):

        all_news = get_news()
        link = kwargs['link']
        if str(link) not in [str(news['link']) for news in all_news]:
            raise Http404
        else:
            news = [news for news in all_news if str(news['link']) == str(link)]
            context = {'created': news[0]['created'], 'text': news[0]['text'], 'title': news[0]['title']}
            return render(request, 'news/news.html', context=context)


class NewsMainView(View):

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        all_news = get_news()

        if q:
            all_news = [news for news in all_news if q.lower() in news['title'].lower()]

        dates = list(set([datetime.datetime.strptime(news['created'], '%Y-%m-%d %H:%M:%S').date() for news in all_news]))
        dates.sort(reverse=True)
        dates_news = {str(date): [news for news in all_news if date == datetime.datetime.strptime(news['created'], '%Y-%m-%d %H:%M:%S').date()] for date in dates}
        context = {'dates_news': dates_news}
        return render(request, 'news/main.html', context=context)


class CreateNewsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        all_news = get_news()
        created = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
        title = request.POST.get('title')
        text = request.POST.get('text')

        while True:
            link = random.randint(100000, 999999)
            if str(link) not in [str(news['link']) for news in all_news]:
                break

        with open(NEWS_JSON_PATH, 'r+') as update_file:
            news_lst = json.load(update_file)
            news_lst.append({"created": created, "text": text, "title": title, "link": link})
            update_file.seek(0)
            json.dump(news_lst, update_file, indent=4)

        return redirect('/news/')
