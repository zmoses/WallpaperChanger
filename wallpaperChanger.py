"""
Wallpaper Changer
Sets your background to a given file
Currently supported OSs:
    Linux with gnome3
"""

from gi.repository import Gio # Linux running Gnome 3+ uses gsettings to change settings

def gnome3_changer(file_path):
    gsettings = Gio.Settings.new('org.gnome.desktop.background')
    gsettings.set_string('picture-uri', 'file://' + file_path)
    gsettings.apply()