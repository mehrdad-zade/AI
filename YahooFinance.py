"""
1. pip install yfinance

"""

import yfinance as yahooFinance  # pip install yfinance
import requests
import json
from urllib.request import urlopen
import bs4 as beautifulSoup  # pip install beautifulsoup4
import lxml.html


class YahooFinance:

    def __init__(self, ticker):
        self.yahoo_data = ""
        self.ticker = ticker

    def getTickerInfo(self, ticker):
        ticker = yahooFinance.Ticker(ticker)
        print(self.string2soup(ticker.info))

    def getNewsHeadlines(self, print_extracted_data):
        url = 'https://finance.yahoo.com/quote/' + self.ticker
        response = requests.get(url)
        if not response.ok:
            print('Status code:', response.status_code)
            raise Exception('Failed to load page {}'.format(url))
        # print(self.html2soup(response.text))
        soup = self.getSoup(response.text)
        # print(soup.title)
        div_tag_news_section = soup.find_all('div', {'id': "quoteNewsStream-0-Stream"})
        links = div_tag_news_section[0].findAll('a')
        for title in links:
            if print_extracted_data:
                print(title.text) # prints news titles
                print(url + title['href']) # prints all the links
            self.yahoo_data += title.text + '. '

    def getYahooData(self):
        return self.yahoo_data


    def html2soup(self, html):
        return beautifulSoup.BeautifulSoup(html, features="lxml").prettify()

    def string2soup(self, str):
        return json.dumps(str, indent=4)

    def getSoup(self, html):
        return beautifulSoup.BeautifulSoup(html, 'html.parser')

"""
yf = YahooFinance('AAPL')
yf.getNewsHeadlines()
yf.getYahooData()
"""