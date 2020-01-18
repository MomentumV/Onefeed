import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from feedgen.feed import FeedGenerator


# each "show" has its own object, that gets updater functions added to it
class PodCast(FeedGenerator):
    def __init__(self):
        """
        This wrapper of FeedGenerator adds the podcast extension at creation.
        """
        super().__init__()
        self.__download = False
        self.load_extension('podcast')

    def set_download(self, download=False):
        if download:
            self.__download = True
        return self.__download


class OnePlacePodCast(PodCast):
    def __init__(self, page=None):
        super().__init__()
        self.link(href='http://oneplace.com', rel='alternate')
        self.language('en')
        self.podcast.itunes_category('Christianity')
        self.pageUrl = page  # this is to be accessible and updated when this class is instanced

    # the pageUrl should be the url to be retrieved during updating.
    def rss_file(self, filename=None, pretty=True):
        if filename is None:
            filename = self.title() + ' rss.xml'
        extensions = True
        encoding = 'UTF-8'
        xml_declaration = True
        super().rss_file(filename, extensions, pretty, encoding, xml_declaration)

    def refresh(self):
        # TODO retrieve page and extract information
        pass
        return


def main():
    page = 'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/'
    RadioTheatre = OnePlacePodCast(page)
    RadioTheatre.dow
    RadioTheatre.title('Radio Theatre')
    RadioTheatre.description('The Weekly broadcast of the award winning audio dramas '
                             'from Focus on the Family, hosted by OnePlace.com')
    RadioTheatre.id(page)

    return RadioTheatre


if __name__ == '__main__':
    main()
