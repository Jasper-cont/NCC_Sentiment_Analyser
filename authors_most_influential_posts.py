import praw
import json
from secrets import secrets
import pprint
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from praw.models import MoreComments
import regex as re


def split_sentences(text, sia):
    pattern = r"\.|\n"
    result_sentences = re.split(pattern, text)

    #Remove this line out when built into main function
    sia = SentimentIntensityAnalyzer()
    sentences_scores_list = []
    for sentence in result_sentences:

        # Analyze the sentiment of the sentence
        sentiment_scores = sia.polarity_scores(sentence)

        if -0.05 > sentiment_scores['compound'] or sentiment_scores['compound'] > 0.05:
            sentences_scores_list.append(sentiment_scores)

    return sentences_scores_list


def calculate_average_scores(score_list):
    added_scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}

    if len(score_list) > 0:

        for score in score_list:
            added_scores['neg'] += score['neg']
            added_scores['neu'] += score['neu']
            added_scores['pos'] += score['pos']
            added_scores['compound'] += score['compound']

        added_scores['neg'] = round(added_scores['neg'] / len(score_list), 3)
        added_scores['neu'] = round(added_scores['neu'] / len(score_list), 3)
        added_scores['pos'] = round(added_scores['pos'] / len(score_list), 3)
        added_scores['compound'] = round(added_scores['compound'] / len(score_list), 3)
    
        return added_scores
    else:
        return None

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
    ticker_pattern = [r'(\$[A-Za-z0-9]{3,6})',r'\b[A-Z]{3,5}\b']
    valid_tickers = []
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
                    if len(post.selftext) < 1:
                        continue
                    tickers_found_1 = re.findall(ticker_pattern[0], post.selftext)
                    # tickers_found_2 = re.findall(ticker_pattern[1], post.selftext)
                    if len(tickers_found_1) > 0:
                        # print("Here1")
                        for ticker in tickers_found_1:
                            if ticker.upper().replace('$', '') in company_tickers:
                                valid_tickers.append(ticker)
                        
                    # if len(tickers_found_2) > 0:
                    #     print("Here2")
                    #     for ticker in tickers_found_2:
                    #         if ticker.upper() in company_tickers:
                    #             valid_tickers.append(ticker)
                    
                    if len(valid_tickers) > 0:
                        post_comments = iter_top_level(post.comments)
                        top_posts.append((author, post.title, post.selftext, post_comments, post.score, list(set(valid_tickers))))
                    
                    valid_tickers = []

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
    #         "vader_lexicon"
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
        # comments_added_scores = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
        # comments_scores_list = []
        print(f"Title: {title}, Title Score: {sia.polarity_scores(title)}, Tickers: {ticker}")
        

        print(f"Content: {content}, Score: {sia.polarity_scores(content)}")

        score_list = split_sentences(content, sia)

        added_scores = calculate_average_scores(score_list)

        comment_scores = []
        for comment in comments:
            comment_score_list = split_sentences(comment.body, sia)
            comment_added_scores = calculate_average_scores(comment_score_list)
            if comment_added_scores:
                comment_scores.append(comment_added_scores)
        average_comment_score = calculate_average_scores(comment_scores)

        print(f"Content score: {added_scores}")
        # print(f"Comment scores: {comment_scores}")
        print(f"Average comment score: {average_comment_score}")
