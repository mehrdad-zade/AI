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

    def getTickerInfo(self, ticker):
        ticker = yahooFinance.Ticker(ticker)
        print(self.string2soup(ticker.info))

    def getNewsHeadlines(self, ticker):
        url = 'https://finance.yahoo.com/quote/' + ticker
        response = requests.get(url)
        if not response.ok:
            print('Status code:', response.status_code)
            raise Exception('Failed to load page {}'.format(url))
        # print(self.html2soup(response.text))
        soup = self.getSoup(response.text)
        # print(soup.title)
        div_tags_news_section = soup.find_all('div', {'id': "quoteNewsStream-0-Stream"})
        for div in div_tags_news_section:
            links = div.findAll('a')
            for a in links:
                #print(url + a['href'])
                if ticker in a.contents[1]:
                    print(a.contents[1])

    def html2soup(self, html):
        return beautifulSoup.BeautifulSoup(html, features="lxml").prettify()

    def string2soup(self, str):
        return json.dumps(str, indent=4)

    def getSoup(self, html):
        return beautifulSoup.BeautifulSoup(html, 'html.parser')


# YahooFinance().getTickerInfo('FB')
YahooFinance().getNewsHeadlines('AAPL')
