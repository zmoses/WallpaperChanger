"""
Reddit Image Downloader
Downloads the top picture(s) on a subreddit
"""

import praw     # An API wrapper for Reddit
import re       # Regular expression support
import requests # Download files via HTTP
import glob     # Used to search files already downloaded
from   bs4 import BeautifulSoup # An HTML parser

def access_reddit(useragent, subreddit, lim):
    r = praw.Reddit(user_agent = useragent)
    return r.get_subreddit(subreddit).get_top(limit = lim)

def download_image(image_url, submission_id, album_id, image_file):
    local_name = 'reddit_%s_album_%s_imgur_%s' % (submission_id, album_id, image_file)
    response = requests.get(image_url)
    if response.status_code == 200:
        print('Downloading %s....' % (local_name))
        with open(local_name, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)
    return local_name

def get_submission(submission):
    # Create a regex object to be used for re.search() later on
    imgur_url_pattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
    if "imgur.com/" not in submission.url:
        # If the Url is not from Imgur
        return
    if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
        # If we've already downloaded this submission
        return

    if 'http://imgur.com/a/' in submission.url:
        # If the image is part of an album....
        albumId = submission.url[len('http://imgur.com/a/'):]
        html_source = requests.get(submission.url).text

        soup = BeautifulSoup(html_source)
        matches = soup.select('.album-view-image-link a')

        files = []
        for match in matches:
            image_url = match['href']
            if '?' in image_url:
                imageFile = image_url[image_url.rfind('/') + 1:image_url.rfind('?')]
            else:
                imageFile = image_url[image_url.rfind('/') + 1:]
            files = files.append(download_image('http:' + match['href'], submission.id, albumId, imageFile))
        return files

    elif 'http://i.imgur.com/' in submission.url:
        # If the image is a direct link....
        mo = imgur_url_pattern.search(submission.url)
        imgur_filename = mo.group(2)
        if '?' in imgur_filename:
            imgur_filename = imgur_filename[:imgur_filename.find('?')]
        return download_image(submission.url, submission.id, 'NA', imgur_filename)

    elif 'http://imgur.com/' in submission.url:
        # If the image is on a page on Imgur as the only image
        html_source = requests.get(submission.url).text
        soup = BeautifulSoup(html_source)
        image_url = soup.select('.image a')[0]['href']
        
        if image_url.startswith('//'):
            image_url = 'http:' + image_url
        imageId = image_url[image_url.rfind('/') + 1:image_url.rfind('.')]

        if '?' in image_url:
            imageFile = image_url[image_url.rfind('/') + 1:image_url.rfind('?')]
        else:
            imageFile = image_url[image_url.rfind('/') + 1:]
        return download_image(image_url, submission.id, 'NA', imageFile)