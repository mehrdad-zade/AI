from Reddit import Reddit
from DataCleansing import DataCleansing
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn
import matplotlib.pyplot as plt
import pandas as pd


class Sentiment:
    def __init__(self, ):
        self.redditData_cleaned = DataCleansing(Reddit().getSubredditComments('tesla')).cleanse()

    def polarity_score_of_words(self):
        sia = SentimentIntensityAnalyzer()
        res = []
        for sentences in self.redditData_cleaned:
            pol_score = sia.polarity_scores(sentences)
            pol_score['words'] = sentences
            res.append(pol_score)
        pd.set_option('display.max_column', None, 'max_colwidth', None)
        df = pd.DataFrame.from_records(res)
        df['label'] = 0
        df.loc[df['compound'] > 0.10, 'label'] = 1
        df.loc[df['compound'] < -0.10, 'label'] = -1
        # print(df)
        # print(df.label.value_counts())
        self.sentiment_representation(df)

    def sentiment_representation(self, df):
        fig, ax = plt.subplots(figsize=(8, 8))
        counts = df.label.value_counts(normalize=True) * 100
        seaborn.barplot(x=counts.index, y=counts, ax=ax)
        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        ax.set_ylabel('Percentage')
        plt.show()


Sentiment().polarity_score_of_words()
