from msgpack import packb, unpackb
from dateutil.parser import parse
from datetime import datetime

from typing import Any


def mp(obj: Any) -> bytes:
    """
    Message Pack
    Pack a Python object using MessagePack
    :param obj: Any Python object
    :return: Packed obj in binary format
    """
    return packb(obj.dict(), use_bin_type=True)


def mup(obj: bytes) -> Any:
    """
    Message UnPack
    Unpacks a MessagePack binary
    :param obj: Packed msgpack binary
    :return: Python object
    """
    return unpackb(obj, encoding='utf-8', raw=True)


def trimto(string: str, n: int = 50) -> str:
    """
    pass
    """
    if not isinstance(string, str):
        string = str(string)
    if len(string) > n:
        string = string[:n - 3] + '...'
    return string


def reddit_time_to_datetime(t: str) -> str:
    return datetime.utcfromtimestamp(float(t)).strftime('%Y-%m-%dT%H:%M:%SZ')


def twitter_time_to_datetime(t: str) -> datetime:
    return parse(t).strftime('%Y-%m-%dT%H:%M:%SZ')


def news_time_to_datetime(t: str) -> datetime:
    return parse(t).strftime('%Y-%m-%dT%H:%M:%SZ')
