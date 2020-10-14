Emojify
=======

Emoji translation for Python.  This project relies on previous works, like [emoji](https://github.com/carpedm20/emoji), [emojilib](https://github.com/muan/emojilib), and [vaderSentiment](https://github.com/cjhutto/vaderSentiment).

The primary differentiator of this work is the incorporation of keyword alternatives to the standard unicode emoji descriptions, which result in more natural translations. The translation can also be randomized if desired.


Example
-------

```
import emojify

emo = emojify.Emojify(exact_match_only=False, randomize=True)

# basic translation
print(emo.emojify('The house is on fire!'))     # > 'The 🏠 is on 🔥!'
print(emo.demojify('The 🏠 is on 🔥!'))         # > 'The house is on fire!'

# targeting sentiment
print(emo.remove_positive_emojis('That new SNL skit 😂😂'))    # > 'That new SNL skit'

print(emo.add_positive_emojis('I cannot believe it!', num=1))   # > 'I cannot believe it! 💪'
print(emo.add_negative_emojis('I cannot believe it!', num=2))   # > 'I cannot believe it! 🙄😱'
print(emo.add_neutral_emojis('I cannot believe it!', num=3))    # > 'I cannot believe it! 🚝🐮🛶'
```

NOTE: Emoji sentiment (polarity) was computed by concatenating the emoji `short_name` and `keywords` and passing them all into `vaderSentiment.SentimentIntensityAnalyzer`.

Installation
------------

Via pip:

```
pip install emoji --upgrade
```

From master branch:

```
$ git clone https://github.com/fabriceyhc/emojify.git
$ cd emojify
$ python setup.py install
```

Roadmap
-------

The following enhancements are planned for sometime in the future. Feel free to reach out / submit pull requests if you want to beat me to it.

1. Creating a static / functional version of the package that does not require the creation of Emojify object.  
2. Incorporating part-of-speech (POS) information during emoji translation, possibly via [spaCy](https://github.com/explosion/spaCy).
3. Using an alternative to VADER for sentiment analysis on the emojis, possibly offering a variety of options.

Authors
-------

Fabrice Harel-Canada / [@fabriceyhc](https://github.com/fabriceyhc)