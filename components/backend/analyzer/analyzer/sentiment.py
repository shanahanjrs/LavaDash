from nltk.sentiment.vader import SentimentIntensityAnalyzer

from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer

from functools import lru_cache
from statistics import fmean

from analysis_utils.models import AnalysisModel

from typing import Dict, Any


class SentimentAnalyzer:
    """
    :returns: analysis_utils.models.AnalysisModel
    {
        "language": lang,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "data": {
            "textblob": t,
            "vader": v
        }
    }
    """
    def __init__(self) -> None:
        self.__vader_sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
        self.__textblob_pattern_analyzer = PatternAnalyzer()

    def __vader_analyze(self, text: str) -> Dict[str, Any]:
        return self.__vader_sentiment_intensity_analyzer.polarity_scores(text)

    def __textblob_analyze(self, text: str) -> Dict[str, Any]:
        return TextBlob(text, analyzer=self.__textblob_pattern_analyzer)

    @lru_cache(maxsize=500)
    def analyze(self, text: str) -> Dict[str, Any]:
        textblob_p = self.__textblob_analyze(text)
        textblob_analysis = {"polarity": textblob_p.polarity, "subjectivity": textblob_p.subjectivity}
        vader = self.__vader_analyze(text)
        vader_analysis = {
            "compound": vader['compound'],
            "neg": vader['neg'],
            "neu": vader['neu'],
            "pos": vader['pos'],
        }

        lang = textblob_p.detect_language()
        polarity = fmean([textblob_p.sentiment.polarity, vader['compound']])
        subjectivity = textblob_p.sentiment.subjectivity
        analysis = AnalysisModel(language=lang,
                                 polarity=polarity,
                                 subjectivity=subjectivity,
                                 data={
                                     "textblob": textblob_analysis,
                                     "vader": vader_analysis
                                 })

        return analysis
