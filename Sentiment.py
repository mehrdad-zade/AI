from Reddit import Reddit
from DataCleansing import DataCleansing
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn
import matplotlib.pyplot as plt
import pandas as pd
from nltk import FreqDist
from wordcloud import WordCloud
import plotly.express


class Sentiment:

    def polarity_score_of_words(self, data):
        sia = SentimentIntensityAnalyzer()
        res = []
        for sentences in data:
            pol_score = sia.polarity_scores(sentences)
            pol_score['words'] = sentences
            res.append(pol_score)
        pd.set_option('display.max_column', None, 'max_colwidth', None)
        df = pd.DataFrame.from_records(res)
        df['label'] = 0
        df.loc[df['compound'] > 0.10, 'label'] = 1
        df.loc[df['compound'] < -0.10, 'label'] = -1
        # print(df)
        print(df.label.value_counts())
        # self.display_sentiment_representation(df)
        return df

    def display_sentiment_representation(self, df):
        fig, ax = plt.subplots(figsize=(8, 8))
        counts = df.label.value_counts(normalize=True) * 100
        seaborn.barplot(x=counts.index, y=counts, ax=ax)
        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        ax.set_ylabel('Percentage')
        plt.show()

    # get top 20 positive or negative words frequencies
    def get_top_20_word_freq(self, df, positive=True):
        if positive:
            positive_indicator = 1
        else:
            positive_indicator = -1
        return FreqDist(list(df.loc[df['label'] == positive_indicator].words)).most_common(20)

    def display_word_cloud(self, df):
        pos_words = [str(p) for p in self.get_top_20_word_freq(df, positive=True)]
        neg_words = [str(p) for p in self.get_top_20_word_freq(df, positive=False)]
        pos_words_str = ' , '.join(pos_words)
        neg_words_str = ' , '.join(neg_words)
        wordcloud_pos = WordCloud(background_color='white').generate(pos_words_str)
        wordcloud_neg = WordCloud().generate(neg_words_str)
        plt.imshow(wordcloud_pos, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        plt.imshow(wordcloud_neg, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def display_bar_chart(self, df):
        pos_freq_df = pd.DataFrame(self.get_top_20_word_freq(df, positive=True))
        pos_freq_df = pos_freq_df.rename(columns={0: 'Bar Graph of Frequent Words', 1: 'Count'}, inplace=False)
        fig = plotly.express.bar(pos_freq_df, x= 'Bar Graph of Frequent Words', y='Count', title='Commonly Used Positive Words By Count')
        fig.show()

    def analysis_method_1(self, query, print_data):
        """
        this method gathers 5 sub-reddits and their top 5 comments and put them all in one string.
        the string is cleaned through emoji removal, tokenizing, stopword removal and lemmatizing.
         then using polarity_score_of_words we build a df which can provide info such as, number of
         pos/neg/neu based on the polarity score of the words.
         if we are interested in building wordCloud or bar charts, they are available too.
        """
        print('--------Reddit Sentiments--------')
        redditData_cleaned = DataCleansing(Reddit().getSubredditComments(search=query, printExtract=print_data)).getClean()
        df = Sentiment().polarity_score_of_words(redditData_cleaned)
        #Sentiment().display_word_cloud(df)
        #Sentiment().display_bar_chart(df)
        #print('Done.')


#Sentiment().analysis_method_1('trump')
