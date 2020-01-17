import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from feedgen.feed import FeedGenerator


# each "show" has its own object, that gets updater functions added to it
class PodCast(FeedGenerator):
    def __init__(self):
        super().__init__()
        self.load_extension('podcast')


# noinspection PyUnresolvedReferences
class OnePlacePodCast(PodCast):
    def __init__(self, page=None):
        super().__init__()
        self.link(href='http://oneplace.com', rel='alternate')
        self.language('en')
        self.podcast.itunes_category('Christianity')

    self.pageUrl = page  # this is to be accessible and updated when this class is instanced

    # the pageUrl should be the url to be retrieved during updating.
    def refresh(self):
        # TODO retrieve page and extract information
        pass
        return

RadioTheatre = OnePlacePodCast('https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/')
