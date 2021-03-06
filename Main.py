from DataCleansing import DataCleansing
from Reddit import Reddit
from Sentiment import Sentiment
from Twitter import TwitterClient
from YahooFinance import YahooFinance

query = 'tesla'
ticker = 'tsla'
print_extracted_data = False


print('--------Reddit Sentiments : ' + query)
redditData_cleaned = DataCleansing(Reddit().getSubredditComments(query, print_extracted_data)).getClean()
Sentiment().analysis_method_1(redditData_cleaned)

print('--------Twitter Sentiments : ' + query)
TwitterClient().main(query, print_extracted_data)

print('--------Yahoo Finance Sentiments : ' + ticker)
yf = YahooFinance(ticker.upper())
yf.getNewsHeadlines(print_extracted_data)
yahooData_cleaned = DataCleansing(yf.getYahooData()).getClean()
Sentiment().analysis_method_1(yahooData_cleaned)


