import redditImageDownloader # To download image
import wallpaperChanger      # To detect and change OS
import os                    # To get current working directory


submissions = redditImageDownloader.access_reddit('WallpaperChanger 0.1', 'wallpapers', 1)
for submission in submissions:
    image_name = redditImageDownloader.get_submission(submission)

if str(image_name) != 'None':
    file_location = os.getcwd() + '/' + str(image_name)
    wallpaperChanger.gnome3_changer(file_location)