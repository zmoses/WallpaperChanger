"""
Downloads the top picture on /r/wallpapers and sets
sets it to your wallpaper.
"""

import praw     # An API wrapper for Reddit
import re       # Regular expression support
import requests # Download files via HTTP
import os
import glob     # Used to search files already downloaded
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

for submission in submissions:
  if "imgur.com/" not in submission.url:
    continue
  if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
    continue

  if 'http://imgur.com/a/' in submission.url:
    albumId = submission.url[len('http://imgur.com/a/'):]
    htmlSource = requests.get(submission.url).text

    soup = BeautifulSoup(htmlSource)
    matches = soup.select('.album-view-image-link a')

    for match in matches:
      imageUrl = match['href']
      if '?' in imageUrl:
        imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
      else:
        imageFile = imageUrl[imageUrl.rfind('/') + 1:]
      localName = 'reddit_%s_album_%s_imgur_%s' % (submission.id, albumId, imageFile)
      downloadImage('http:' + match['href'], localName)
      
  elif 'http://i.imgur.com/' in submission.url:
    mo = imgurUrlPattern.search(submission.url)
    imgurFilename = mo.group(2)
    if '?' in imgurFilename:
      imgurFilename = imgurFilename[:imgurFilename.find('?')]
    localName = 'reddit_%s_album_NA_imgur_%s' % (submission.id, imgurFilename)
    downloadImage(submission.url, localName)

  elif 'http://imgur.com/' in submission.url:
    htmlSource = requests.get(submission.url).text
    soup = BeautifulSoup(htmlSource)
    imageUrl = soup.select('.image a')[0]['href']
    
    if imageUrl.startswith('//'):
      imageUrl = 'http:' + imageUrl
    imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

    if '?' in imageUrl:
      imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
    else:
      imageFile = imageUrl[imageUrl.rfind('/') + 1]

    localName = 'reddit_%s_album_NA_imgur_%s' % (submission.id, imageFile)
    downloadImage(imageUrl, localName)