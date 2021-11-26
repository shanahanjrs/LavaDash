import datetime

from typing import Optional, Union, Dict, List
from pydantic import BaseModel


class Headline(BaseModel):
    """
    A "Normalized" Type that will hold either a Twitter, Reddit, or News "story"
    type: twitter/reddit/news
    data: array of all scraped tweets/posts/stories
    date_time: time we scraped
    term: Query term we searched for
    """
    type: str
    data: Union[Dict, List]
    date_time: Optional[datetime.datetime] = None
    term: str

    def __post_init__(self):
        if self.date_time is None:
            self.date_time = datetime.datetime.now()


class DataPoint(BaseModel):
    """
    Standard InfluxDB DatePoint in JSON form:
    {
        "measurement": "analysis_event",
        "time": "2009-11-10T23:00:00Z",
        "tags": {
            "type": "twitter"
        },
        "fields": {
            "language": "en",
            "subjectivity": "0.3",
            "polarity": "0.45",
            "author": "JohnIsSuperCool",
            "title": "My Name is Flynn and John is Cool"
        }
    }
    """
    measurement: str
    time: str
    tags: Dict
    fields_value: Dict[str, str]

    class Config:
        fields = {'fields_value': 'fields'}


class AnalysisModel(BaseModel):
    """
    {
        "language": lang,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "data": {
            "textblob": {},
            "vader": {}
        }
    }
    """
    language: str
    polarity: float
    subjectivity: float
    data: dict
