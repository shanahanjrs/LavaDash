"""
Main scraping service and daemon
"""

from asyncio import get_event_loop
import multiprocessing
from os import environ
import time

from flask import Flask
from flask import jsonify

from scraper.scraper_twitter.twitter_scraper import TwitterScraper
twitter_api = TwitterScraper()

from scraper.scraper_reddit.reddit_scraper import RedditScraper
reddit_api = RedditScraper()

from scraper.scraper_news.news_scraper import NewsScraper
news_api = NewsScraper()

from scraper.daemon import start_daemon

import logging
logging.basicConfig(level=logging.DEBUG)

from redis import Redis
r = Redis(host=environ.get('REDIS_HOST', 'localhost'),
          port=environ.get('REDIS_PORT', 6379))

# Instantiate Flask
app = Flask(__name__)

# TODO move `new_term` and `get_terms` to a new Terms service


@app.route('/search/terms/<string:term>', methods=['GET', 'POST'])
def new_term(term: str) -> str:
    """
    Add a new Term that will be scraped every 60s
    :param term: (string) New term to be scraped and analyzed
    :return:
    """
    # TODO validate term?
    # TODO remove the GET - should be POST only
    r.sadd('scrapeTerms', term)
    return jsonify({"status": 200, "message": "ok"})


@app.route('/search/terms')
def get_terms() -> str:
    """
    Get scrape terms
    :return:
    """
    terms = r.smembers('scrapeTerms')
    terms = [t.decode("utf-8") for t in terms]
    return jsonify({"status": 200, "message": "ok", "data": terms})


@app.route('/search/twitter/<string:query>', methods=['GET'])
def search_twitter(query: str) -> str:
    data = twitter_api.search(query).dict()
    return jsonify({"status": 200, "data": data})


@app.route('/search/reddit/<string:query>', methods=['GET'])
def search_reddit(query: str) -> str:
    """
    comments 	Provides an instance of CommentForest.
    created_utc 	Time the submission was created, represented in Unix Time.
    is_original_content 	Whether or not the submission has been set as original content.
    permalink 	A permalink for the submission.
    """
    data = reddit_api.search(query).dict()
    return jsonify({"status": 200, "data": data})


@app.route('/search/news/<string:query>')
def search_news(query: str) -> str:
    data = news_api.search(query).dict()
    return jsonify({"status": 200, "message": "ok", "data": data})


def start_flask() -> None:
    logging.debug('starting flask')
    app.run()


# For some reason the main-guard swallows multiprocessing so run without for now
start_daemon()


if __name__ == '__main__':
    start_flask()
