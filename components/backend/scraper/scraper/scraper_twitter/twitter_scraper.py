"""
Twitter Obj:
{
      "created_at": "Thu Aug 20 17:26:33 +0000 2020",
      "hashtags": [],
      "id": 1296498873838579716,
      "id_str": "1296498873838579716",
      "lang": "en",
      "retweet_count": 4209,
      "retweeted_status": {
        "created_at": "Thu Aug 20 15:35:01 +0000 2020",
        "favorite_count": 7310,
        "hashtags": [],
        "id": 1296470804058832899,
        "id_str": "1296470804058832899",
        "lang": "en",
        "retweet_count": 4209,
        "source": "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
        "text": "Donald Trump Jr. praised We Build The Wall and Brian Kolfage at a 2018 event: \"This is private enterprise at its fi\u2026 https://t.co/zZOwoZuKeG",
        "truncated": true,
        "urls": [
          {
            "expanded_url": "https://twitter.com/i/web/status/1296470804058832899",
            "url": "https://t.co/zZOwoZuKeG"
          }
        ],
        "user": {
          "created_at": "Wed Jun 29 16:44:57 +0000 2011",
          "description": "Reporter at CNN's K-File.Flex cam winner at a Nets game. \ud83c\udde6\ud83c\uddf1 Arb\u00ebresh\u00eb\ud83c\uddee\ud83c\uddf9\ud83c\uddf5\ud83c\uddf1. Cat Friend. Gchat: Andrew.w.Kaczynski@gmail.com Insta:AndyKaczynski",
          "favourites_count": 54586,
          "followers_count": 330746,
          "friends_count": 4965,
          "id": 326255267,
          "id_str": "326255267",
          "listed_count": 6954,
          "location": "New York, USA",
          "name": "andrew kaczynski\ud83e\udd14",
          "profile_background_color": "3B94D9",
          "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
          "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
          "profile_banner_url": "https://pbs.twimg.com/profile_banners/326255267/1462030182",
          "profile_image_url": "http://pbs.twimg.com/profile_images/1282750073139597314/Re5bOzdP_normal.jpg",
          "profile_image_url_https": "https://pbs.twimg.com/profile_images/1282750073139597314/Re5bOzdP_normal.jpg",
          "profile_link_color": "1B95E0",
          "profile_sidebar_border_color": "FFFFFF",
          "profile_sidebar_fill_color": "DDEEF6",
          "profile_text_color": "333333",
          "profile_use_background_image": true,
          "screen_name": "KFILE",
          "statuses_count": 3421,
          "url": "https://t.co/oSGSbsz3Us",
          "verified": true
        },
        "user_mentions": []
      }
"""

from twitter import Api
from analysis_utils.models import Headline

import datetime
from os import environ


class TwitterScraper:
    def __init__(self) -> None:
        self.__api_key = environ.get('TWITTER_API_KEY', '')
        self.__api_secret = environ.get('TWITTER_API_SECRET', '')
        self.__bearer_token = environ.get('TWITTER_BEARER_TOKEN', '')
        self.__access_token = environ.get('TWITTER_ACCESS_TOKEN', '')
        self.__access_token_secret = environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')
        self.api_client = Api(consumer_key=self.__api_key,
                              consumer_secret=self.__api_secret,
                              access_token_key=self.__access_token,
                              access_token_secret=self.__access_token_secret)
        self.count = 25
        self.minutes_back = 1
        self.from_time = (datetime.datetime.now() - datetime.timedelta(minutes=self.minutes_back))
        self.yyyy = self.from_time.strftime('%Y')
        self.mm = self.from_time.strftime('%m')
        self.dd = self.from_time.strftime('%d')

    def search(self, query: str) -> Headline:

        res = self.api_client.GetSearch(
            raw_query=f"q={query}%20&result_type=recent&since={self.yyyy}-{self.mm}-{self.dd}&count={self.count}")
        tweets = [tweet.AsDict() for tweet in res]

        headline = Headline(**{'type': 'twitter', 'data': tweets, 'term': query})

        return headline
