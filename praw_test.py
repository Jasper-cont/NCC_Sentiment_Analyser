import praw

reddit = praw.Reddit(
"bot1"
)

print(reddit.read_only)





# assume you have a praw.Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("redditdev")


#for submission in reddit.subreddit("redditdev").hot(limit=10):
 #   print(submission.title)

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)
# Output: a subreddit for discussion of ...



# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)
    # Output: the submission's title
    print(submission.score)
    # Output: the submission's score
    print(submission.id)
    # Output: the submission's ID
    print(submission.url)
    # Output: the URL the submission points to or the submission's URL if it's a self post


submission = reddit.submission("14oevki")

print('submission_title: ', submission.title)

'''
There are several ways to obtain a redditor (a Redditor instance). Two of the most common ones are:
via the author attribute of a Submission or Comment instance
via the redditor() method of Reddit
'''


'''





'''