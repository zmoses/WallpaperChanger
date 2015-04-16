"""
Downloads the top picture on /r/wallpapers and sets
sets it to your wallpaper.
"""

import praw
import pyimgur

user_agent = "WallpaperChanger 0.1"
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("wallpapers")

for submission in subreddit.get_top(limit = 5):
  print "Title: ", submission.title
  print "URL:   ", submission.url, "\n"

CLIENT_ID = #todo
im = pyimgur.Imgur(CLIENT_ID)

