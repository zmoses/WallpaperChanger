"""
Downloads an image from reddit and sets it as your wallpaper
Currently supported OSs:
    Linux running Gnome 3

ToDo:
    Fix unclosed socket
    Download and set single image out of an album
    Add more OSs
"""
import praw     # An API wrapper for Reddit
import re       # Regular expression support
import requests # Download files via HTTP
import glob     # Used to search files already downloaded
from   os            import path          # Used for getting file locations
from   gi.repository import Gio           # Edit settings for Gnome 3+
from   bs4           import BeautifulSoup # An HTML parser
from   urllib3       import HTTPConnectionPool

class ImageDownloader(object):
    def __init__(self, useragent, subreddit):
        self.reddit_connection = praw.Reddit(user_agent = useragent)
        self.subreddit = subreddit
        self.submissions = self.reddit_connection.get_subreddit(subreddit)
        self.downloaded_images = []

    def top(self, lim):
        return self.submissions.get_top(limit = lim)

    def hot(self, lim):
        return self.submissions.get_hot(limit = lim)

    def download_image(self, image_url, submission_id, album_id, image_file):
        local_name = 'reddit_%s_album_%s_imgur_%s' % (submission_id, album_id, image_file)
        response = requests.get(image_url)
        if response.status_code == 200:
            print('Downloading %s....' % (local_name))
            with open(local_name, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)
        self.downloaded_images = self.downloaded_images + [local_name]

    def should_download(self, submission):
        if "imgur.com/" not in submission.url:
            # If the Url is not from Imgur
            return False
        if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
            # If we've already downloaded this submission
            return False
        return True

    def get_id(self, url):
        # Gets id from Imgur + the file extension (.jpg, .png, etc.)
        if '?' in url:
            image_file = url[url.rfind('/') + 1:url.rfind('?')]
        else:
            image_file = url[url.rfind('/') + 1:]
        return image_file

    def get_album_submission(self, submission):
        # Method is called if the image is part of an album
        album_id = submission.url[len('http://imgur.com/a/'):]
        html_source = requests.get(submission.url).text
        soup = BeautifulSoup(html_source)
        matches = soup.select('.album-view-image-link a')

        for match in matches:
            image_url = match['href']
            image_file = self.get_id(image_url)
            self.download_image('http:' + image_url, submission.id, album_id, image_file)

    def get_single_submission(self, submission):
        # Method is called if the image is on a page on Imgur as the only image
        # If the url includes the file extension (which links to the image url)
        if '.' in submission.url[submission.url.rfind('/') + 1:]:
            self.get_single_image(submission)
            return

        html_source = requests.get(submission.url).text
        soup = BeautifulSoup(html_source)
        image_url = soup.select('.image a')[0]['href']
        
        if image_url.startswith('//'):
            image_url = 'http:' + image_url
        imageId = image_url[image_url.rfind('/') + 1:image_url.rfind('.')]

        image_file = self.get_id(image_url)
        self.download_image(image_url, submission.id, 'NA', image_file)

    def get_single_image(self, submission):
        # Method is called if the url is a direct url to the image
        imgur_filename = self.get_id(submission.url)
        self.download_image(submission.url, submission.id, 'NA', imgur_filename)

    def analyze_submission(self, submission):
        if 'http://i.imgur.com/' in submission.url:
            self.get_single_image(submission)

        elif 'http://imgur.com/a/' in submission.url:
            self.get_album_submission(submission)

        elif 'http://imgur.com' in submission.url:
            self.get_single_submission(submission)

class WallpaperChanger(object):
    def gnome3_changer(self, file_path):
        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', 'file://' + file_path)
        gsettings.apply()

if __name__ == '__main__':
    reddit_session = ImageDownloader('WallpaperChanger 0.1', 'wallpapers')
    submissions = reddit_session.top(25)
    selection = 1
    options = {}
    
    for submission in submissions:
        if reddit_session.should_download(submission):
            options[selection] = submission
            print(str(selection) + ': ' + submission.title)
            selection += 1
        if selection == 6:
            break
    print('6: Keep current')

    image_selection = int(input('Select an option: '))

    if image_selection in range(1,6):
        reddit_session.analyze_submission(options[image_selection])

        if str(reddit_session.downloaded_images) != []:
            file_location = path.realpath(reddit_session.downloaded_images[0])
            wallpaper = WallpaperChanger()
            wallpaper.gnome3_changer(file_location)

    reddit_session.close()