import praw
import json
import pprint
import itertools
from secrets import secrets


def ExtractRedditorsKarma(subreddit_names, post_limit, reddit):
    author_karma = {}

    for subr in subreddit_names:

        author_karma[subr] = {}

        # Get the subreddit instance
        subreddit = reddit.subreddit(subr)

        # Get the top posts from the subreddit
        top_posts = subreddit.top(limit=post_limit)

        # Create a dictionary to store author karma
        no_link_karma_count = 0
        no_comment_karma_count = 0
        # Iterate over the posts and track author karma
        for post in top_posts:
            author = post.author
            if author:
                if author not in author_karma:
                    # the name of the redditor
                    # redditor_name = "spez"
                    
                    # instantiating the Redditor class
                    # redditor = reddit.redditor(author_name)
                    author_data = reddit.redditor(author.name)
                    # pprint.pprint(vars(author_data))
                    # pprint.pprint(vars(redditor))
                    try:
                        author_karma[subr][author.name] = author_data.link_karma
                    except:
                        author_karma[subr][author.name] = 0
                        no_link_karma_count += 1
                    try:
                        author_karma[subr][author.name] += author_data.comment_karma
                    except:
                        no_comment_karma_count += 1

        errors = f"{subr}: No link Karma count: {no_link_karma_count}, No comment Karma count: {no_comment_karma_count}"

    return author_karma, errors

            # author_data = reddit.redditor(author.name)
            # author_karma = 0
            # # Fetch submissions and add their scores to author_karma
            # for submission in author.submissions.new(limit=10):
            #     author_karma += submission.score

            # # Fetch comments and add their scores to author_karma
            # for comment in author.comments.new(limit=10):
            #     author_karma += comment.score


if __name__ == '__main__':
    reddit_s = secrets()
    sec_dict = reddit_s.reddit_secrets()

    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=sec_dict["CLIENT_ID"],
        client_secret=sec_dict["CLIENT_SECRET"],
        user_agent=sec_dict["USERNAME"],
        username=sec_dict["USERNAME"],
        password=sec_dict["PASSWORD"]
    )

    # Specify the subreddit you want to pull posts from
    subreddit_names = ["Stockmarket", "pennystocks", "EducatedInvesting", "wallstreetbets"]
    post_limit = 20
    author_karma, errors = ExtractRedditorsKarma(subreddit_names, post_limit, reddit)

    with open('candidate_redditors.json', 'r') as f:
        historical_redditors = f.read()

    if len(historical_redditors) < 1:
        historical_redditors = {}
    else:
        historical_redditors = json.loads(historical_redditors)

    for subr_key in author_karma.keys():
        if subr_key not in historical_redditors.keys():
            historical_redditors[subr_key] = {}

        for author_key in author_karma[subr_key].keys():
            if int(author_karma[subr_key][author_key]) > 1000:
                historical_redditors[subr_key][author_key] = author_karma[subr_key][author_key]

    # pprint.pprint(historical_redditors)

    with open('candidate_redditors.json', 'w') as f:
        f.write(json.dumps(historical_redditors))


# for submission in reddit.subreddit("all").hot(limit=3):
#     print(submission.title)

# url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
# submission = reddit.submission(url=url)

# for comment in subreddit.stream.comments(skip_existing=True):
#     print(comment)
