
class Story:
    """
    A base object for _normalizing_ things like News stories, Tweets, Reddit comments, etc...
    holds some text and runs Vader + TextBlob (Pattern) on it and normalizes the output
    """

    def __init__(self, text):
        self.text = text

    def analyze(self):
        pass

    def __repr__(self):
        return '%s(%s)' % self.__class__.__name__, self.text

    def __str__(self):
        return self.text
