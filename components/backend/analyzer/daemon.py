from analysis_utils.models import DataPoint

import asyncio
import multiprocessing
from redis import Redis
from os import environ
from analysis_utils import (mup, twitter_time_to_datetime, reddit_time_to_datetime, news_time_to_datetime, trimto)
from analyzer.sentiment import SentimentAnalyzer
from influxdb import InfluxDBClient
from typing import Dict, Any, AnyStr

import logging
logging.basicConfig(level=logging.DEBUG)

DAEMON_ITERATION_TIME = int(environ.get('DAEMON_ITERATION_TIME', 60))


class AnalyzerDaemon:
    def __init__(self) -> None:
        self.r_analyze_list = 'toAnalyze'
        self.redis = Redis(host=environ.get('REDIS_HOST', 'localhost'), port=environ.get('REDIS_PORT', 6379))
        self.sentiment_analyzer = SentimentAnalyzer()
        self.influxdb_client = InfluxDBClient(
            host=environ['INFLUXDB_HOST'],
            port=environ['INFLUXDB_PORT'],
            username=environ['INFLUXDB_ADMIN_USER'],    # Dont use admin in the future
            password=environ['INFLUXDB_ADMIN_PASSWORD'],
            ssl=False,
            verify_ssl=False)
        self.influxdb_db_name = 'analyses'

        self.check_influx_db_exists()
        self.influxdb_client.switch_database(self.influxdb_db_name)

    def get_next_headline(self) -> AnyStr:
        """
        https://redis.io/commands#list
        """
        ret = mup(self.redis.brpop(self.r_analyze_list)[1])  # 0th item is the name of the list echo'd back to us
        logging.debug('>>>> analyzer::daemon::get_next_headline: %s' % trimto(ret))
        logging.debug('>>>> analyzer::daemon::get_next_headline::return type: %s' % type(ret))

        return ret

    def check_influx_db_exists(self) -> bool:
        """
        Checks the correct db exists for sending results
        """
        if {'name': self.influxdb_db_name} not in self.influxdb_client.get_list_database():
            logging.error('InfluxDB is missing the %s DB!' % self.influxdb_db_name)
            return False
        return True

    async def influxdb_push(self, data_point: DataPoint) -> None:
        """
        TODO batch these writes and figure out better way to call the `.dict()` method on these Pydantic models
        """
        if not isinstance(data_point, list):
            data_point = [data_point.dict(by_alias=True)]
        else:
            data_point = [dp.dict(by_alias=True) for dp in data_point]
        logging.debug('== influxdb_push :: PUSHING TO INFLUX: ========================================================')
        logging.debug('%s' % data_point)
        logging.debug('===============================================================================================')
        self.influxdb_client.write_points(data_point, protocol='json')

    async def analyze_twitter(self, message: str) -> None:
        """
        Performs sentiment analysis on a Tweet
        :param message: (Obj) Object to analyze
        :returns: None
        """

        for post in message['data']:

            try:
                analysis = self.sentiment_analyzer.analyze(post['text'])
            except Exception as e:
                logging.error(e)
                continue

            data_point = DataPoint(time=twitter_time_to_datetime(post['created_at']),
                                   measurement='analysis_event',
                                   tags={'term': message['term']},
                                   fields={
                                       'polarity': analysis.polarity,
                                       'language': analysis.language,
                                       'subjectivity': analysis.subjectivity,
                                       'author': post.get('user', {}).get('screen_name', '$$EMPTY'),
                                       'title': post['text'],
                                       'body': '$$EMPTY',
                                       'type': 'twitter'
                                   })

            await asyncio.gather(self.influxdb_push(data_point))

    async def analyze_reddit(self, message: str) -> None:
        """
        Performs sentiment analysis on a Reddit post's body
        :param message: (Obj) Object to analyze
        :returns: None
        """

        for post in message['data']:

            try:
                analysis = self.sentiment_analyzer.analyze(post['body'])    # or title? or both?
            except Exception as e:
                logging.error(e)
                continue

            data_point = DataPoint(time=reddit_time_to_datetime(post['datetime']),
                                   measurement='analysis_event',
                                   tags={'term': message['term']},
                                   fields={
                                       'polarity': analysis.polarity,
                                       'language': analysis.language,
                                       'subjectivity': analysis.subjectivity,
                                       'author': post.get('author', '$$EMPTY'),
                                       'title': post['title'],
                                       'body': post['body'],
                                       'type': 'reddit'
                                   })

            await asyncio.gather(self.influxdb_push(data_point))

    async def analyze_news(self, message: str) -> None:
        """
        Performs sentiment analysis on a news article's title
        :param message: (Obj) Object to analyze
        :returns: None
        """

        for post in message['data']['articles']:

            try:
                analysis = self.sentiment_analyzer.analyze(post['title'])    # or body? or both?
            except Exception as e:
                logging.error(e)
                continue

            data_point = DataPoint(time=news_time_to_datetime(post['publishedAt']),
                                   measurement='analysis_event',
                                   tags={'term': message['term']},
                                   fields={
                                       'language': analysis.language,
                                       'subjectivity': analysis.subjectivity,
                                       'polarity': analysis.polarity,
                                       'author': post.get('author', '$$EMPTY'),
                                       'title': post['title'],
                                       'body': post['content'],
                                       'type': 'news'
                                   })

            await asyncio.gather(self.influxdb_push(data_point))

    async def analyze(self, obj: Dict[str, Any]) -> None:
        #logging.debug('---------------------------------------------------------------------------')
        #logging.debug('> obj.keys(): %s' % obj.keys())
        #logging.debug('---------------------------------------------------------------------------')
        logging.debug(obj)

        if obj['type'] == 'reddit':
            await asyncio.gather(self.analyze_reddit(obj))

        elif obj['type'] == 'twitter':
            await asyncio.gather(self.analyze_twitter(obj))

        elif obj['type'] == 'news':
            logging.debug('-------------------------------------------------------------------------------------------')
            logging.debug('-- Got a News type object -----------------------------------------------------------------')
            logging.debug('-------------------------------------------------------------------------------------------')
            await asyncio.gather(self.analyze_news(obj))

        else:
            logging.error('got an unidentified obj to analyze. skipping...')


def daemon_runner() -> None:
    d = AnalyzerDaemon()

    while True:
        headline_dict = d.get_next_headline()
        logging.debug('>>>> analyzer::daemon::headline_dict::type %s' % type(headline_dict))
        # data = headline_dict['data']
        # asyncio.run(d.analyze(data))
        asyncio.run(d.analyze(headline_dict))


def start_daemon() -> None:
    x = multiprocessing.Process(name='analyzer_daemon', target=daemon_runner, daemon=True)
    logging.debug('starting daemon process')
    x.start()
