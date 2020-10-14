"""
Unit tests for emoji-translate
"""

import emoji_translate

def test_lookup():
	emo = emojify.Translate(exact_match_only=True, randomize=False)
	for emoji, desc in emo.emojis[['char', 'short_name']].values.tolist():
	    desc_lookup  = emo.demojify(emoji)
	    assert desc  == desc_lookup, "%s != %s" % (desc, desc_lookup)
	    #emoji_lookup = emo.emojify(desc)
	    # assert emoji == emoji_lookup, "%s != %s" % (emoji, emoji_lookup)