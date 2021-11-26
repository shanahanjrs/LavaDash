"""
News obj:
 {
    "articles": [
      {
        "author": null,
        "content": "Chat with us in Facebook Messenger. Find out what's happening in the world as it unfolds.",
        "description": "Former senior Trump administration official Miles Taylor says he is concerned that President Donald Trump will use litigation to make the 2020 race difficult for electors to certify.",
        "publishedAt": "2020-08-20T12:49:22Z",
        "source": {
          "id": "cnn",
          "name": "CNN"
        },
        "title": "Ex-DHS official: I fear Trump will do this to make the election difficult",
        "url": "https://www.cnn.com/videos/politics/2020/08/20/miles-taylor-trump-election-concerns-newday-vpx.cnn",
        "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/200820082616-miles-taylor-08202020-super-tease.jpg"
      }
    ],
    "status": "ok",
    "totalResults": 1171
  }
"""
from newsapi import NewsApiClient
import datetime

from os import environ

from analysis_utils.models import Headline


class NewsScraper:
    def __init__(self) -> None:
        self.__api_key = environ.get('NEWSAPI_API_KEY', '')
        self.api_client = NewsApiClient(api_key=self.__api_key)
        self.minutes_back = 120 if environ.get('FLASK_ENV', '') == 'development' else 1
        self.from_time = (datetime.datetime.now() - datetime.timedelta(minutes=self.minutes_back))
        self.page_s = 20 if environ.get('FLASK_ENV', '') == 'development' else 100
        self.page_n = 1

    def search(self, query: str) -> Headline:
        news_stories = self.api_client.get_everything(q=query,
                                                      language='en',
                                                      from_param=self.from_time,
                                                      page_size=self.page_s)
        headline = Headline(**{'type': 'news', 'data': news_stories, 'term': query})

        return headline
