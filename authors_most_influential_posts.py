import praw
import json
from secrets import secrets
import nltk
import pprint
from nltk.sentiment import SentimentIntensityAnalyzer
from praw.models import MoreComments
import regex as re
# from top_level_load import TopLvlComments

def iter_top_level(comments):
    more_comments = []
    for top_level_comment in comments:
        if isinstance(top_level_comment, MoreComments):
            more_comments.append(top_level_comment.comments if not isinstance(top_level_comment.comments(), MoreComments) else None)
        else:
            more_comments.append(top_level_comment)
    return more_comments


def get_top_posts_by_authors(reddit, authors_sorted, post_limit_per_author):
    top_posts = []
    ticker_pattern = r'\b[$]?[A-Z0-9]{2,}\b'
    tickers_found = []
    for subreddit in authors_sorted.keys():
        for author in authors_sorted[str(subreddit)].keys():
            try:
                # author = author[0]
                print('author: ', author)
                redditor = reddit.redditor(author)

                # Get the top posts by this author
                author_top_posts = redditor.submissions.top(limit=post_limit_per_author)

                # Append each post to the list and extract the top level comments
                for post in author_top_posts:
                    print("0")
                    tickers_found = re.findall(ticker_pattern, post.selftext)
                    if len(tickers_found) > 0:
                        print("1")
                        if tickers_found[0] in company_tickers:
                            print("2")
                            post_comments = iter_top_level(post.comments)
                            print("3")
                            top_posts.append((author, post.title, post.selftext, post_comments, post.score, tickers_found[0]))
                            print("4")

                    else: 
                        print("1")
                        post_comments = iter_top_level(post.comments)
                        print("2")
                        top_posts.append((author, post.title, post.selftext, post_comments, post.score, False))
                        print("3")

            except Exception as e:
                print(f"Failed to get posts for author {author}: {str(e)}")

    # Sort the posts by score in descending order
    top_posts.sort(key=lambda x: x[2], reverse=True)

    return top_posts


if __name__ == "__main__":
    #
    with open('candidate_redditors.json', 'r') as f:
        historical_redditors = f.read()
    if len(historical_redditors) < 1:
        historical_redditors = {}
    else:
        historical_redditors = json.loads(historical_redditors)

    with open('company_ticker.json', 'r') as f:
        company_tickers = json.loads(f.read())

    # Create a Reddit instance
    reddit_s = secrets()
    sec_dict = reddit_s.reddit_secrets()
    reddit = praw.Reddit(
        client_id=sec_dict["CLIENT_ID"],
        client_secret=sec_dict["CLIENT_SECRET"],
        user_agent=sec_dict["USERNAME"],
        username=sec_dict["USERNAME"],
        password=sec_dict["PASSWORD"]
    )

    # Use the function
    top_posts = get_top_posts_by_authors(reddit, historical_redditors, 1)

    # Sentiment Analyse the top posts
    # nltk.download([
    #         "vader_lexicon",
    #         "stopwords"
    #     ])
    # text = """
    # For some quick analysis, creating a corpus could be overkill.
    # If all you need is a word list,
    # there are simpler ways to achieve that goal."""

    # tokenised_text = nltk.word_tokenize(text)
    # pprint.pprint(tokenised_text)
    sia = SentimentIntensityAnalyzer()

    for index, (author, title, content, comments, score, ticker) in enumerate(top_posts):
        # pprint.pprint(f"Index: {index}, Author: {author}, Post Title: {title}, Post Score: {score}, Content: {content}")
        
        '''
        For better accuracy I want to setup VADER to rate individual sentences instead of full posts (or comments)
        '''
        print(len(content))
        print(comments[0].body)
        print(f"Title: {title}, Title Score: {sia.polarity_scores(title)}, Body Score: {sia.polarity_scores(content)}, First comment Score: {sia.polarity_scores(comments[0].body)}, Ticker: {ticker}")