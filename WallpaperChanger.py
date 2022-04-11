import urllib.request # import api access modules
import urllib.parse
import urllib.error
from json import loads

import ctypes # import system modules
from win32con import SPIF_UPDATEINIFILE, SPI_SETDESKWALLPAPER, SPIF_SENDCHANGE
from os import getcwd

from random import randint

# Enter your pixabay api-key below
API_KEY = '' # Configure API-KEY, KEYWORD and IMAGE_SAVE_PATH
KEYWORD = 'Green nature'
IMAGE_SAVE_PATH = getcwd() + '\\CurrentWallpaper.jpg'

# Pixabay API url
SERVICE_URL = 'https://pixabay.com/api/'  


class PixabayAPIHandle(): # Handles Pixabay API
    def __init__(self) -> None:
        self._setup_user_agent()
    
    def _setup_user_agent(self):  # setups user agent to deal with HTTP 403 error
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')] 
        urllib.request.install_opener(opener)

    def get_url(self): # sets and returns url
        url = SERVICE_URL + '?key=' + API_KEY + '&' + urllib.parse.urlencode({'q': KEYWORD, 'orientation': 'horizontal', 'order': 'ec', 'editors_choice': 'true','min_width':'1280','min_height':'720', 'per_page': 200, 'pretty': 'true'})
        return url

    def get_image(self): # gets url and then saves image into IMAGE_SAVE_PATH
        url_req = urllib.request.Request(self.get_url())
        url_object = urllib.request.urlopen(url_req)

        data = url_object.read().decode()
        self.images_json = loads(data) # loads data as json

        image_url = self.images_json['hits'][self._random_value()]['largeImageURL'] # extract image url from json
        urllib.request.urlretrieve(image_url, filename = IMAGE_SAVE_PATH) # saves image


    def _random_value(self): # returns random index value, for random selection of image
        return randint(0, len(self.images_json['hits'])-1)

def set_wallpaper(path): # makes system calls to change wallpaper
    changed = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoA(
        SPI_SETDESKWALLPAPER, 0, path.encode(), changed) 

if __name__ == '__main__':
    image_api = PixabayAPIHandle()
    image_api.get_image() # saves image
    set_wallpaper(IMAGE_SAVE_PATH)

