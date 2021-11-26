"""
 class praw.models.Submission(reddit: Reddit, id: Optional[str] = None, url: Optional[str] = None, _data: Optional[Dict[str, Any]] = None)

    A class for submissions to reddit.

    Typical Attributes

    This table describes attributes that typically belong to objects of this class. Since attributes are dynamically provided (see Determine Available Attributes of an Object), there is not a guarantee that these attributes will always be present, nor is this list necessarily complete.
    Attribute 	Description
    author 	Provides an instance of Redditor.
    clicked 	Whether or not the submission has been clicked by the client.
    comments 	Provides an instance of CommentForest.
    created_utc 	Time the submission was created, represented in Unix Time.
    distinguished 	Whether or not the submission is distinguished.
    edited 	Whether or not the submission has been edited.
    id 	ID of the submission.
    is_original_content 	Whether or not the submission has been set as original content.
    is_self 	Whether or not the submission is a selfpost (text-only).
    link_flair_template_id 	The link flair’s ID, or None if not flaired.
    link_flair_text 	The link flair’s text content, or None if not flaired.
    locked 	Whether or not the submission has been locked.
    name 	Fullname of the submission.
    num_comments 	The number of comments on the submission.
    over_18 	Whether or not the submission has been marked as NSFW.
    permalink 	A permalink for the submission.
    poll_data 	A PollData object representing the data of this submission, if it is a poll submission.
    score 	The number of upvotes for the submission.
    selftext 	The submissions’ selftext - an empty string if a link post.
    spoiler 	Whether or not the submission has been marked as a spoiler.
    stickied 	Whether or not the submission is stickied.
    subreddit 	Provides an instance of Subreddit.
    title 	The title of the submission.
    upvote_ratio 	The percentage of upvotes from all votes on the submission.
    url 	The URL the submission links to, or the permalink if a selfpost.
"""

import praw
from analysis_utils.models import Headline
from os import environ


class RedditScraper:
    def __init__(self) -> None:
        self.__app_name = 'analyzer'
        self.__client_id = environ.get('REDDIT_CLIENT_ID', '')
        self.__client_secret = environ.get('REDDIT_CLIENT_SECRET', '')
        # https://github.com/praw-dev/praw/blob/master/praw/models/reddit/subreddit.py#L758
        self.timeframe = 'hour'    # TODO `hour` is as small as we can get..
        self.api_client = praw.Reddit(client_id=self.__client_id,
                                      client_secret=self.__client_secret,
                                      user_agent=self.__app_name)

    def search(self, query: str) -> Headline:
        posts = []
        res = self.api_client.subreddit("all").search(query, time_filter=self.timeframe)
        for post in res:
            if not post.is_self:
                # Skip non-text posts
                continue

            posts.append({
                "title": post.title,
                "body": post.selftext,
                "url": post.url,
                "upvote_ratio": post.upvote_ratio,
                "subreddit": str(post.subreddit),
                "score": post.score,
                "permalink": post.permalink,
                "author": str(post.author),
                "datetime": str(post.created_utc),
            })
        headline = Headline(**{'type': 'reddit', 'data': posts, 'term': query})

        return headline
