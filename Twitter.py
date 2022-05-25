import Secrets
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import re

"""
1. get twitter development account setup: https://developer.twitter.com/en
2. within the account, request to get access token and secret
3. within the account, upgrade to "Elevated" access

"""


class TwitterClient:

    def __init__(self):
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(Secrets.TWITTER_API_KEY, Secrets.TWITTER_API_KEY_SECRET)
            # set access token and secret
            self.auth.set_access_token(Secrets.TWITTER_ACC_TOKEN, Secrets.TWITTER_ACC_TOKEN_SECRET)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        api = self.authenticate()
        try:
            # call twitter api to fetch tweets
            fetched_tweets = api.search(q=query, count=count)
            print(fetched_tweets)
        except:
            print("cannot connect to Twitter API..")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.errors.TweepyException as e:
            # print error (if any)
            print("Error : " + str(e))

    def main(self, query, print_data):
        # creating object of TwitterClient Class
        api = TwitterClient()
        # calling function to get tweets
        tweets = api.get_tweets(query=query, count=200)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        #print('--------Twitter Sentiments--------')
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of neutral tweets
        print("0    {} % ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))
        # percentage of positive tweets
        print("1    {} %".format(100 * len(ptweets) / len(tweets)))
        # percentage of negative tweets
        print("-1    {} %".format(100 * len(ntweets) / len(tweets)))


        if print_data:
            # printing first 5 positive tweets
            print("\n\nPositive tweets:")
            for tweet in ptweets[:10]:
                print(tweet['text'])

            # printing first 5 negative tweets
            print("\n\nNegative tweets:")
            for tweet in ntweets[:10]:
                print(tweet['text'])

