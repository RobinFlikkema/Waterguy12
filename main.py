import calendar
import os

import datetime
from time import sleep

import praw
from praw.exceptions import APIException

reddit = praw.Reddit(client_id='xx',
                     client_secret='xx',
                     password='xx',
                     user_agent='waterguy12 tag bot liker',
                     username='xx')

print(reddit.user.me())
while True:
    # start where left off
    print("Reading where i left off")
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    for comment in reddit.redditor('waterguy12_tag_bot').comments.new(limit=1000):
        d = datetime.datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        if "u/waterguy12" in comment.body and comment.created_utc > unixtime - 86400 and comment.id not in comments_replied_to:
            comment.upvote()
            not_replied = True
            while not_replied:
                try:
                    comment.reply("Good bot")
                    comments_replied_to.append(comment.id)
                    not_replied = False
                except APIException as e:
                    print(e)
                    print("Sleeping 600 seconds")
                    sleep(600)
                    pass
            print("replied to: " + comment.link_permalink)
            sleep(30)
        else:
            break

    # Save where left off
    print("Saving where i left off")
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")
