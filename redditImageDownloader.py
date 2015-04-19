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
from   bs4 import BeautifulSoup # An HTML parser

def access_reddit(user_agent, subreddit, lim):
    r = praw.Reddit(user_agent = user_agent)
    submissions = r.get_subreddit(subreddit).get_top(limit = lim)

def download_image(imageUrl, submission_id, album_id, image_file):
    localName = 'reddit_%s_album_%s_imgur_%s' % (submission_id, album_id, image_file)
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s....' % (localName))
        with open(localName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

def get_submission(submissions):
    # Create a regex object to be used for re.search() later on
    imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
    if "imgur.com/" not in submission.url:
        # If the Url is not from Imgur
        return
    if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
        # If we've already downloaded this submission
        return

    if 'http://imgur.com/a/' in submission.url:
        # If the image is part of an album....
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
            download_image('http:' + match['href'], submission.id, albumId, imageFile)
      
    elif 'http://i.imgur.com/' in submission.url:
        # If the image is a direct link....
        mo = imgurUrlPattern.search(submission.url)
        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            imgurFilename = imgurFilename[:imgurFilename.find('?')]
        download_image(submission.url, submission.id, 'NA', imgurFilename)

    elif 'http://imgur.com/' in submission.url:
        # If the image is on a page on Imgur as the only image
        htmlSource = requests.get(submission.url).text
        soup = BeautifulSoup(htmlSource)
        imageUrl = soup.select('.image a')[0]['href']
        
        if imageUrl.startswith('//'):
            imageUrl = 'http:' + imageUrl
        imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

        if '?' in imageUrl:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
        else:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:]
        download_image(imageUrl, submission.id, 'NA', imageFile)

if __name__ == '__main__':
    access_reddit('WallpaperChanger 0.1', 'wallpapers', 5)
    for submission in submissions:
        get_submission(submission)