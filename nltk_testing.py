import nltk
import pprint
from nltk.sentiment import SentimentIntensityAnalyzer

# Sentiment Analyse the top posts
nltk.download([
        "vader_lexicon",
        "stopwords",
        "punkt",
        "state_union"
    ])

text = """
For some quick analysis, creating a corpus could be overkill.
If all you need is a word list,
there are simpler ways to achieve that goal."""

words = [w for w in nltk.corpus.state_union.words() if w.isalpha()]

# tokenised_text = nltk.word_tokenize(words)
# Use .isalpha() to filter out punctuation
fd = nltk.FreqDist(words)
print(fd.most_common(3)) #For code
print(fd.tabulate(3)) #For humains
print(fd["America"])

lower_fd = nltk.FreqDist([w.lower() for w in fd])

text = nltk.Text(words)

# text.concordance("america", lines=5)
# Concordance ignores cases

# concordance_list = text.concordance_list("america", lines=2)
# for entry in concordance_list:
#     print(entry.line)

# Text class has some interesting features .vocab() is one
# words = nltk.word_tokenize("""Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.""")

# text = nltk.Text(words)
# fd = text.vocab() # Equiv to frequency distribution
# fd.tabulate(3)

# Also v useful for finding collocations (series of words that frequently appear together) with simple function calls
finder = nltk.collocations.TrigramCollocationFinder.from_words(words)
print(finder.ngram_fd.most_common(2))
print(finder.ngram_fd.tabulate(2))
# pprint.pprint(tokenised_text)

# pprint.pprint(lower_fd)


# The built in pre-trained sentiment analyzer is called VADER
sia = SentimentIntensityAnalyzer()
print(sia.polarity_scores("Wow, NLTK is really powerful!"))
