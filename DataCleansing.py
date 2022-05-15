import emoji
from nltk.tokenize import RegexpTokenizer
import en_core_web_sm  # 1) pip install spacy, 2) python -m spacy download en
from nltk.stem import WordNetLemmatizer


class DataCleansing:
    def __init__(self, data):
        self.social_media_data = data

    # Removing Emojis
    def removeEmojis(self):
        self.social_media_data = emoji.replace_emoji(self.social_media_data, replace='')

    # Tokenizing, removing links etc.
    def tokenize(self):
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
        self.social_media_data = tokenizer.tokenize(self.social_media_data)
        self.social_media_data = [word.lower() for word in self.social_media_data]

    # Removing stopwords
    def removeStopwords(self):
        nlp = en_core_web_sm.load()
        all_stopwords = nlp.Defaults.stop_words
        self.social_media_data = [word for word in self.social_media_data if not word in all_stopwords]

    # Normalizing words via lemmatizing
    def normalize_lemmatize(self):
        lemmantizer = WordNetLemmatizer()
        self.social_media_data = ([lemmantizer.lemmatize(word) for word in self.social_media_data])

    def getClean(self):
        # order of below operations matters
        self.removeEmojis()
        self.tokenize()
        self.removeStopwords()
        return self.social_media_data

# DataCleansing().cleanse()
