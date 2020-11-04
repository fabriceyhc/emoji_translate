import string
import regex as re
import pandas as pd
import random

from emoji import unicode_codes, get_emoji_regexp, emoji_lis

from os import path
pwd = path.abspath(path.dirname(__file__))

class Translator:
    def __init__(self, exact_match_only=True, 
        exclude_stopwords=True, randomize=True):
        self.exact_match_only = exact_match_only 
        self.exclude_stopwords = exclude_stopwords
        if self.exclude_stopwords:
            from spacy.lang.en.stop_words import STOP_WORDS
            stopwords = STOP_WORDS
        else:
            stopwords = set()
        self.stopwords = stopwords
        self.randomize = randomize

        # load emojis to DataFrame
        self.emojis = pd.read_json(path.join(pwd, 'data/merged_emojis.json'))

    # emojify
    def emojify(self, string):
        pattern = re.compile(u'([a-zA-Z0-9\\+\\-_&ô’Åéãíç()#*]+)')
        def replace(match):
            word = match.group(0)
            if word in self.stopwords:
                return word
            return self.get_emoji(word)
        return pattern.sub(replace, string)

    def get_emoji(self, word):
        emojis = self.get_emojis(word)
        if 'exact' in emojis:
            return emojis['exact']
        if 'alts' in emojis:
            idx = random.randint(0, len(emojis['alts'])-1) if self.randomize else 0
            return emojis['alts'][idx]
        return word

    def get_emojis(self, word):
        df = self.emojis
        emojis = {}
        _word = word.translate(str.maketrans('', '', string.punctuation))
        exact = df[df['short_name'].values == _word]['char']
        if exact.any():
            emojis['exact'] = exact.values[0]
        if not self.exact_match_only:
            alt = df[df['keywords'].apply(lambda x: _word in x)]['char']
            if alt.any():
                emojis['alts'] = alt.values.tolist()
        return emojis

    def get_df_by_word(self, word):
        df = self.emojis
        _word = word.translate(str.maketrans('', '', string.punctuation))
        df1 = df[df['short_name'].values == _word]
        df2 = df[df['keywords'].apply(lambda x: _word in x)]
        return pd.concat((df1,df2))

    # demojify
    def demojify(self, string):
        def replace(match):
            emoji = match.group(0)
            return self.get_word(emoji)
        return re.sub(u'\ufe0f','',(get_emoji_regexp().sub(replace, string)))

    def get_word(self, emoji):
        words = self.get_words(emoji)
        if 'exact' in words:
            if '_' not in words['exact']:
                return words['exact']
        if 'alts' in words:
            idx = random.randint(0, len(words['alts'])-1) if self.randomize else 0
            return words['alts'][idx]
        return emoji

    def get_words(self, emoji):
        df = self.get_df_by_emoji(emoji)
        words = {}
        exact = df['short_name']
        if exact.any():
            words['exact'] = exact.values[0]
        alt = df['keywords']
        if alt.any():
            words['alts'] = alt.values.tolist()
        return words

    def get_df_by_emoji(self, emoji):
        df = self.emojis
        return df[df['char'].values == emoji]

    # Sentiment (polarity) functions

    def remove_emoji_by_polarity(self, string, p_rng=[-1,1]):
        for emoji_data in emoji_lis(string)[::-1]:
            i, emoji = emoji_data.values()
            _polarity = self.get_df_by_emoji(emoji)['polarity'].iloc[0]
            if p_rng[0] <= _polarity <= p_rng[1]:
                string = string[:i] + '' + string[i + 1:].lstrip()
        return string.rstrip()

    def remove_positive_emojis(self, string):
        return self.remove_emoji_by_polarity(string, [(1/3), 1])

    def remove_negative_emojis(self, string):
        return self.remove_emoji_by_polarity(string, [-1, -(1/3)])
            
    def remove_neutral_emojis(self, string):
        return self.remove_emoji_by_polarity(string, [-(1/3), (1/3)])

    def sample_emoji_by_polarity(self, p_rng, num=1):
        return self.emojis[self.emojis['polarity'].apply(
            lambda x: p_rng[0] <= x <= p_rng[1])].sample(num)['char'].values.tolist()
    
    def add_positive_emojis(self, string, num=1):
        return string + ' ' + ''.join(self.sample_emoji_by_polarity([0.05, 1], num))

    def add_negative_emojis(self, string, num=1):
        return string + ' ' + ''.join(self.sample_emoji_by_polarity([-1, -0.05], num))

    def add_neutral_emojis(self, string, num=1):
        return string + ' ' + ''.join(self.sample_emoji_by_polarity([-0.05, 0.05], num))