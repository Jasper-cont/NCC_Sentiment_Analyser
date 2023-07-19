import praw
import json
#
with open('candidate_redditors.json', 'r') as f:
        historical_redditors = f.read()
if len(historical_redditors) < 1:
        historical_redditors = {}
else:
    historical_redditors = json.loads(historical_redditors)

# authors_sorted here will be the sorted karma list of users
# authors_sorted sorted is a json

def get_top_posts_by_authors(reddit, authors_sorted, post_limit_per_author):
    top_posts = []

    for subreddit in authors_sorted:
        for author in authors_sorted[f"{subreddit}"]:
            try:
                author = author[0]
                print('author: ', author)
                redditor = reddit.redditor(author)

                # Get the top posts by this author
                author_top_posts = redditor.submissions.top(limit=post_limit_per_author)

                # Append each post to the list
                for post in author_top_posts:
                    top_posts.append((author, post.title, post.score))

            except Exception as e:
                print(f"Failed to get posts for author {author}: {str(e)}")

    # Sort the posts by score in descending order
    top_posts.sort(key=lambda x: x[2], reverse=True)

    return top_posts



# Get the top 10 authors from your previous step
#top_authors = [author for author, karma in ]

# Create a Reddit instance
reddit = praw.Reddit(
"bot1"
)

# Use the function
top_posts = get_top_posts_by_authors(reddit, historical_redditors, 10)

# Print the top posts
for author, title, score in top_posts:
    print(f"Author: {author}, Post Title: {title}, Post Score: {score}")
