import praw
import json
from secrets import secrets
import nltk
import pprint
from nltk.sentiment import SentimentIntensityAnalyzer
from praw.models import MoreComments
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
                    post_comments = iter_top_level(post.comments)
                    top_posts.append((author, post.title, post.selftext, post_comments, post.score))

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

    # authors_sorted here will be the sorted karma list of users
    # authors_sorted sorted is a json



    # Get the top 10 authors from your previous step
    #top_authors = [author for author, karma in ]

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
    # print(top_posts)

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

    for index, (author, title, content, comments, score) in enumerate(top_posts):
        # pprint.pprint(f"Index: {index}, Author: {author}, Post Title: {title}, Post Score: {score}, Content: {content}")
        print(len(content))
        print(comments[0].body)
        print(f"Title: {title}, Title Score: {sia.polarity_scores(title)}, Body Score: {sia.polarity_scores(content)}, First comment Score: {sia.polarity_scores(comments[0].body)}")