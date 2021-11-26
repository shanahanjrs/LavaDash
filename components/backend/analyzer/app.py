import os

from flask import Flask
from flask import jsonify

import time

from analyzer.sentiment import SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer()

import logging
logging.basicConfig(level=logging.DEBUG)

from daemon import start_daemon

# from redis import Redis
# r = Redis(
#     host=os.environ['REDIS_HOST'],
#     port=os.environ['REDIS_PORT']
# )

# Start API
app = Flask(__name__)


@app.route('/sentiment/<string:text>', methods=['GET', 'POST'])
def sentiment(text: str) -> str:

    t_start = time.time()
    analysis = sentiment_analyzer.eval(text)
    t_end = time.time()
    elapsed = t_end - t_start

    return jsonify({
        "status": 200,
        "input": text,
        "data": analysis,
        "elapsed": elapsed
    })


def start_flask() -> None:
    logging.debug('starting flask for analyzer')
    app.run()


start_daemon()

if __name__ == '__main__':
    start_flask()
