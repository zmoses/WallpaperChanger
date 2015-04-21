import praw     # An API wrapper for Reddit
import re       # Regular expression support
import requests # Download files via HTTP
import glob     # Used to search files already downloaded
import os       # Used for editing file locations
from   gi.repository import Gio           # Edit settings for Gnome 3+
from   bs4           import BeautifulSoup # An HTML parser

class ImageDownloader(object):
    def __init__(self, useragent, subreddit):
        self.reddit_connection = praw.Reddit(user_agent = useragent)
        self.subreddit = subreddit
        self.submissions = r.get_subreddit(subreddit)
        self.downloaded_images = []

    def top(lim):
        return self.submissions.get_top(limit = lim)

    def hot(lim):
        return self.submissions.get_hot(limit = lim)

    def download_image(image_url, submission_id, album_id, image_file):
        local_name = 'reddit_%s_album_%s_imgur_%s' % (submission_id, album_id, image_file)
        response = requests.get(image_url)
        if response.status_code == 200:
            print('Downloading %s....' % (local_name))
            with open(local_name, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)
        return local_name

    def should_download(submission):
        if "imgur.com/" not in submission.url:
            # If the Url is not from Imgur
            return False
        if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
            # If we've already downloaded this submission
            return False
        return True

    def get_submission(submission):
        if 'http://imgur.com/a/' in submission.url:
            # If the image is part of an album....
            album_id = submission.url[len('http://imgur.com/a/'):]
            html_source = requests.get(submission.url).text

            soup = BeautifulSoup(html_source)
            matches = soup.select('.album-view-image-link a')

            for match in matches:
                image_url = match['href']
                if '?' in image_url:
                    image_file = image_url[image_url.rfind('/') + 1:image_url.rfind('?')]
                else:
                    image_file = image_url[image_url.rfind('/') + 1:]
                downloaded_images = downloaded_images.append(download_image('http:' + match['href'], submission.id, album_id, image_file))

        elif 'http://i.imgur.com/' in submission.url:
            # Create a regex object to be used for .search()
            imgur_url_pattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
            # If the image is a direct link....
            mo = imgur_url_pattern.search(submission.url)
            imgurFilename = mo.group(2)
            if '?' in imgurFilename:
                imgurFilename = imgurFilename[:imgurFilename.find('?')]
            return download_image(submission.url, submission.id, 'NA', imgurFilename)

        elif 'http://imgur.com/' in submission.url:
            # If the image is on a page on Imgur as the only image
            html_source = requests.get(submission.url).text
            soup = BeautifulSoup(html_source)
            image_url = soup.select('.image a')[0]['href']
            
            if image_url.startswith('//'):
                image_url = 'http:' + image_url
            imageId = image_url[image_url.rfind('/') + 1:image_url.rfind('.')]

            if '?' in image_url:
                image_file = image_url[image_url.rfind('/') + 1:image_url.rfind('?')]
            else:
                image_file = image_url[image_url.rfind('/') + 1:]
            return download_image(image_url, submission.id, 'NA', image_file)

class WallpaperChanger(object):
    def gnome3_changer(file_path):
        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', 'file://' + file_path)
        gsettings.apply()



if __name__ == '__main__':
    submissions = access_reddit('WallpaperChanger 0.1', 'wallpapers', 1)
    for submission in submissions:
        image_name = get_submission(submission)

    if str(image_name) != 'None':
        file_location = os.getcwd() + '/' + str(image_name)
        gnome3_changer(file_location)