import tweepy
from secrets import secrets

# Get your Twitter API credentials from https://developer.twitter.com/en/apps
twit_s = secrets()
sec_dict = twit_s.twitter_secrets()
CONSUMER_KEY = sec_dict['API_KEY']
CONSUMER_SECRET = sec_dict['API_SECRET']
ACCESS_TOKEN = sec_dict['ACESS_TOKEN']
ACCESS_TOKEN_SECRET = sec_dict['ACESS_SECRET']

# Create a Tweepy API object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Search for tweets that mention stocks and were written by Elon Musk
tweets = api.search_tweets(q="stocks -filter:retweets -filter:links -filter:replies from:elonmusk", count=1)

# Print the tweets
for tweet in tweets:
  print(tweet.text)
