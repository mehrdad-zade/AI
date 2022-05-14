"""
API request - Reddit

1- goto https://www.reddit.com/prefs/apps and "create another app"
2- fill up the form, and get the personal use script and secret
"""

import requests
import pandas as pd
from IPython.display import display
import Secrets


class RedditData:
    def __init__(self, ):
        self.REDDIT_PERSONAL_USE_SCRIPT = Secrets.REDDIT_PERSONAL_USE_SCRIPT
        self.SECRET_TOKEN = Secrets.REDDIT_SECRET_TOKEN
        self.USERNAME = Secrets.REDDIT_USERNAME
        self.PASSWORD = Secrets.REDDIT_PASSWORD
        self.NUMBER_OF_RETURNED_ROWS = 5
        self.LIMIT_RESPONSE_COUNT = 25

    # Request a temporary OAuth token from Reddit. We need our username and password for this
    def authenticate(self, ):
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        auth = requests.auth.HTTPBasicAuth(self.REDDIT_PERSONAL_USE_SCRIPT, self.SECRET_TOKEN)

        # here we pass our login method (password), username, and password
        data = {'grant_type': 'password',
                'username': self.USERNAME,
                'password': self.PASSWORD}

        # setup our header info, which gives reddit a brief description of our app
        headers = {'User-Agent': 'MyBot/0.0.1'}

        # send our request for an OAuth token
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']

        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        return headers

    def prettifyRes(self, res):
        df = pd.DataFrame()  # initialize dataframe
        # loop through each post retrieved from GET request
        i = 0
        for post in res.json()['data']['children']:
            # append relevant data to dataframe
            tmp_df = pd.DataFrame(
                {
                    'subreddit_id': post['data']['subreddit_id'],
                    'subreddit': post['data']['subreddit'],
                    'subreddit_subscribers': post['data']['subreddit_subscribers'],
                    'id': post['data']['id'],
                    'title': post['data']['title'],
                    #'selftext': post['data']['selftext'],
                    'ups': post['data']['ups'],
                    'downs': post['data']['downs'],
                    'score': post['data']['score'],
                    'likes': post['data']['likes'],
                    'num_comments': post['data']['num_comments']
                }, index=[i + 1]
            )
            i += 1
            df = pd.concat([df, tmp_df])
        return df.head(self.NUMBER_OF_RETURNED_ROWS)

    def getRes(self, search, subReddit):
        """
        :param reqType:
            'r/python/hot'
            'r/python/new'
            'r/python/best'
            'r/python/top'

        :return:
            IPython.displays
        """
        headers = self.authenticate()
        # while the token is valid (~2 hours) we just add headers=headers to our requests
        api = 'https://oauth.reddit.com/r/' + search + '/' + subReddit
        res = requests.get(api, headers=headers, params={'limit': self.LIMIT_RESPONSE_COUNT})
        display(self.prettifyRes(res).to_string())


RedditData().getRes(search='msft', subReddit='top')
