import asyncio
import multiprocessing
import time
from scraper.scraper_twitter.twitter_scraper import TwitterScraper
from scraper.scraper_reddit.reddit_scraper import RedditScraper
from scraper.scraper_news.news_scraper import NewsScraper
from redis import Redis
from os import environ
from analysis_utils import mp, trimto
from analysis_utils.models import Headline

from typing import Any, List

import logging
logging.basicConfig(level=logging.DEBUG)

DAEMON_ITERATION_TIME = int(environ.get('DAEMON_ITERATION_TIME', 60))


class ScraperDaemon:
    def __init__(self) -> None:
        self.twitter_api = TwitterScraper()
        self.reddit_api = RedditScraper()
        self.news_api = NewsScraper()
        self.r_analysis_list = 'toAnalyze'
        self.scrape_terms_set_name = 'scrapeTerms'
        self.redis = Redis(host=environ.get('REDIS_HOST', 'localhost'), port=environ.get('REDIS_PORT', 6379))

    def redis_push(self, content: Headline) -> None:
        """
        https://redis.io/commands#list
        """
        logging.debug('>>>> scraper::daemon::redis_push::content: %s' % trimto(content, 25))
        logging.debug('>>>> scraper::daemon::redis_push::content::type: %s' % type(content))
        self.redis.lpush(
            self.r_analysis_list,
            mp(content)
        )

    def get_scrape_terms(self) -> List[str]:
        terms = self.redis.smembers(self.scrape_terms_set_name)
        return [t.decode("utf-8") for t in terms]

    async def scrape_twitter(self, term: str) -> None:
        res = self.twitter_api.search(term)
        self.redis_push(res)

    async def scrape_reddit(self, term: str) -> None:
        res = self.reddit_api.search(term)
        self.redis_push(res)

    async def scrape_news(self, term: str) -> None:
        res = self.news_api.search(term)
        self.redis_push(res)

    async def scrape(self, term: str) -> None:
        await asyncio.gather(self.scrape_twitter(term), self.scrape_reddit(term), self.scrape_news(term))


def daemon_runner() -> None:
    d = ScraperDaemon()
    logging.debug('========================================= ! NOTE ! ================================================')
    logging.debug('=== If the following array is empty you will NOT scrape anything... ===============================')
    logging.debug('=== daemon runner started. Terms as of this moment:\n%s' % d.get_scrape_terms())
    logging.debug('===================================================================================================')

    while True:
        for term in d.get_scrape_terms():
            asyncio.run(d.scrape((str(term))))

        time.sleep(DAEMON_ITERATION_TIME)


def start_daemon() -> None:
    x = multiprocessing.Process(name='scraper_daemon', target=daemon_runner, daemon=True)
    logging.debug('starting daemon')
    x.start()
