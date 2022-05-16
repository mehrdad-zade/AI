from Sentiment import Sentiment
from Twitter import TwitterClient

query = 'elon+musk'

Sentiment().analysis_method_1(query, print_data=False)
TwitterClient().main(query, print_data=False)
