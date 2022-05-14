"""
API request - Reddit

1- goto https://www.reddit.com/prefs/apps and "create another app"
2- fill up the form, and get the personal use script and secret
"""
import praw
import pandas as pd
from tabulate import tabulate
import Secrets


class Reddit:

    # Request a temporary OAuth token from Reddit
    def authenticate(self, ):
        reddit = praw.Reddit(client_id=Secrets.REDDIT_PERSONAL_USE_SCRIPT,
                             client_secret=Secrets.REDDIT_SECRET_TOKEN,
                             user_agent=Secrets.REDDIT_USERNAME)
        return reddit

    def extract(self, voteType):
        df = pd.DataFrame()  # initialize dataframe
        # loop through each post retrieved from GET request
        i = 0
        for submission in voteType:
            submission.comment_sort = 'top'
            submission.comment_limit = 5
            submission.comments.replace_more(limit=0)  # remove MoreComments
            comments = ""
            for comment in submission.comments:
                comments += comment.body
            # append relevant data to dataframe
            tmp_df = pd.DataFrame(
                {
                    'subreddit_id': submission.id,
                    'title': submission.title,
                    'ups': submission.ups,
                    'downs': submission.downs,
                    'score': submission.score,
                    'likes': submission.likes,
                    'num_comments': submission.num_comments,
                    'comments': comments
                }, index=[i + 1]
            )
            i += 1
            df = pd.concat([df, tmp_df])
        print(tabulate(df, showindex=False, headers=df.columns))

    def getSubredditComments(self, search):
        reddit = self.authenticate()
        subreddit = reddit.subreddit(search)
        # sub reddit type
        hot = subreddit.hot(limit=5)
        top = subreddit.top(limit=5)
        rising = subreddit.rising(limit=5)
        new = subreddit.new(limit=5)
        self.extract(voteType=top)


Reddit().getSubredditComments('tesla')
