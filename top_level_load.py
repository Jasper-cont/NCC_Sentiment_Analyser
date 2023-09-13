import praw
from praw.models import MoreComments

class TopLvlComments:

    def __init__(self):
        pass

    def gather_more_comments(self, submission):
        top_level_comment_count = 0
        more_comments = []
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                more_comments.append(top_level_comment)
            else:
                top_level_comment_count += 1

        print(f"Comments: {top_level_comment_count}, MoreComments objects: {len(more_comments)}")
        return more_comments

    def get_comments(self, submission):
        # get the initial MoreComments list
        more_comments = gather_more_comments(submission)
        # loop until the list is empty, ie, there are no top level MoreComments objects left
        while more_comments:
            # grab the first one, just in case there's more than one for some reason
            more_comment = more_comments.pop()

            # call the fetch method to get all the comments from the API
            new_comments = more_comment.comments(update=False)

            count_requests += 1

            # insert all new comments into the tree
            for comment in new_comments:
                # if it's a MoreComments object, but the parent isn't the submission, then it belongs somewhere else in the tree
                # normally PRAW just throws it at the bottom anyway, since it will fetch all the comments and then figure out
                # where they go. We don't want to fetch these child comments, so we throw this away
                if isinstance(comment, MoreComments) and comment.parent_id.startswith('t1_'):
                    continue
                submission.comments._insert_comment(comment)

            # remove this MoreComments item from the tree
            submission.comments._comments.remove(more_comment)

            # iterate through the top level tree again to find the new MoreComments object
            more_comments = gather_more_comments(submission)

        return submission