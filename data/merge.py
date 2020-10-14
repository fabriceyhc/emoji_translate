import os
import pandas as pd 
from emoji import unicode_codes
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():

	merge_file = 'merged_emojis.json'
	if os.path.exists(merge_file):
		print('Emoji dataset already created: {}.'.format(os.path.abspath(merge_file)))
		return False

	analyser = SentimentIntensityAnalyzer()

	# [emojis] from emojilib (https://github.com/muan/emojilib/blob/master/emojis.json) | 1570 emojis
	df1 = pd.read_json('emojis.json', encoding='utf8').T
	df1 = df1.reset_index().rename(columns={'index': 'short_name'})
	# df1 = df1.explode(column='keywords')
	df1['short_name'] = df1['short_name'].str.replace('_', ' ')
	df1['keywords'] = df1['keywords'].apply(lambda _list: [x.replace('_', ' ') for x in _list])

	# [emojis] from vaderSentiment (https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/emoji_utf8_lexicon.txt) | 3570 emojis
	# df2 = pd.read_csv('emoji_utf8_lexicon.txt', delimiter='\t', header=None, names=['char', 'long_name'])
	# df2['long_name'] = df2['long_name'].str.replace(': ', ' with ')

	# [emojis] from emoji (https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py) | 3859 emojis
	df2 = pd.DataFrame.from_dict(unicode_codes.EMOJI_UNICODE, orient='index', columns=['char'])
	df2.reset_index(inplace=True)
	df2.rename(columns={'index':'long_name'}, inplace=True)
	df2['long_name'] = df2['long_name'].str.replace(':', '')
	df2['long_name'] = df2['long_name'].str.replace('[\-\_]', ' ')

	df = pd.merge(df1, df2, how='right', on='char')
	df["short_name"] = df["short_name"].fillna(df["long_name"])
	df.fillna('', inplace=True)

	df['polarity'] = df[['short_name', 'keywords']].apply(
	    lambda x: [x['short_name']] + list(x['keywords']), axis=1).apply(
	        lambda x: analyser.polarity_scores(' '.join(x))['compound'])

	cols = ['char', 'short_name', 'long_name', 'keywords', 'polarity']
	df[cols].to_json(merge_file)

	print('Emoji dataset created: {}.'.format(os.path.abspath(merge_file)))
	return True

if __name__ == '__main__':
	main()