"""
Downloads the top picture on /r/wallpapers and sets
sets it to your wallpaper.
"""

import praw     # An API wrapper for Reddit
import re       # Regular expression support
import requests # Download files via HTTP
import os
import glob
import sys
from bs4 import BeautifulSoup # An HTML parser

def downloadImage(imageUrl, localName):
  response = requests.get(imageUrl)
  if response.status_code == 200:
    print('Downloading %s....' % (localName))
    with open(localName, 'wb') as fo:
      for chunk in response.iter_content(4096):
        fo.write(chunk)

user_agent = "WallpaperChanger 0.1"
r = praw.Reddit(user_agent = user_agent)
submissions = r.get_subreddit("wallpapers").get_top(limit = 5)

# Create a regex object to be used for re.search() and re.match()
imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
