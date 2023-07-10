import praw
import json
import pprint
from secrets import secrets


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
subreddit_name = 'Stockmarket'

# Get the subreddit instance
subreddit = reddit.subreddit(subreddit_name)

post_limit = 10

# Get the top posts from the subreddit
top_posts = subreddit.top(limit=post_limit)

# Create a dictionary to store author karma
author_karma = {}
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
                author_karma[author.name] = author_data.link_karma
            except:
                author_karma[author.name] = 0
                no_link_karma_count += 1
            try:
                author_karma[author.name] += author_data.comment_karma
            except:
                no_comment_karma_count += 1

            # author_data = reddit.redditor(author.name)
            # author_karma = 0
            # # Fetch submissions and add their scores to author_karma
            # for submission in author.submissions.new(limit=10):
            #     author_karma += submission.score

            # # Fetch comments and add their scores to author_karma
            # for comment in author.comments.new(limit=10):
            #     author_karma += comment.score

sorted_authors = sorted(author_karma.items(), key=lambda x: x[1], reverse=True)
pprint.pprint(sorted_authors)
print(f"No link Karma count: {no_link_karma_count}, No comment Karma count: {no_comment_karma_count}")

# print(f"Link Karma: {link_karma}")
# print(f"Comment Karma: {comment_karma}")

# print(author_karma)
# Sort authors by karma in descending order
# sorted_authors = sorted(author_karma.items(), key=lambda x: x[1], reverse=True)

# Print the authors with the highest karma
# for author, karma in sorted_authors[:5]:  # Change 5 to the desired number of authors
#     print(f"Author: {author.name}, Karma: {karma}")


# for submission in reddit.subreddit("all").hot(limit=3):
#     print(submission.title)

# url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
# submission = reddit.submission(url=url)

# for top_level_comment in submission.comments:
#     print(top_level_comment.body)

# for comment in subreddit.stream.comments(skip_existing=True):
#     print(comment)

# # Set the number of posts you want to retrieve
# post_limit = 10

# # Get the top posts from the subreddit
# top_posts = subreddit.top(limit=post_limit)

# # Iterate over the posts and print their titles
# for post in top_posts:
#     print(post.title)
