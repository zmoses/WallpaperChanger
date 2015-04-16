"""
Downloads the top picture on /r/wallpapers and sets
sets it to your wallpaper.
"""

import praw # An API wrapper for Reddit
import pyimgur # An API wrapper for Imgur
from bs4 import BeautifulSoup # An HTML parser

user_agent = "WallpaperChanger 0.1"
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("wallpapers")

for submission in subreddit.get_top(limit = 5):
  # print "Title: ", submission.title
  # print "URL:   ", submission.url, "\n"

# Unique for each application:
CLIENT_ID = "7df853035f99c0a"
CLIENT_SECRET = "5c91dd04dc51fbfb0bf0c4e773f9563e6169b36c"

im = pyimgur.Imgur(CLIENT_ID)
image = im.get_image('S1jmapR')
print image.link