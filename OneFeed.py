# import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
# from bs4 import BeautifulSoup
import time
from feedgen.feed import FeedGenerator


# each "show" has its own object, that gets updater functions added to it
class PodCast(FeedGenerator):
    def __init__(self):
        """
        This wrapper of FeedGenerator adds the podcast extension at creation.
        """
        super().__init__()
        self.__download = False # this property is to signal if the podcast should save the file when it updates
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
        self.titlexpath = '//div[@class="overlay2"]//h2'  # might need customizing for each page?
        self.descxpath = '//div[@class="description"]'
        self.audioxpath = '//audio'

    # the pageUrl should be the url to be retrieved during updating.
    def rss_file(self, filename=None, pretty=True):
        if filename is None:
            filename = self.title() + ' rss.xml'
        extensions = True
        encoding = 'UTF-8'
        xml_declaration = True
        super().rss_file(filename, extensions, pretty, encoding, xml_declaration)

    def refresh(self):
        """
        Starts a headless Firefox browser to load the page and render the source. That source is passed into
        BeautifulSoup to easily extract the latest link, title, description
        :return:
        """
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        browser = Firefox(options=opts)
        browser.get(self.pageUrl)
        time.sleep(4)
        ep_title = browser.find_element_by_xpath(self.titlexpath).text
        ep_description = browser.find_element_by_xpath(self.descxpath).text
        ep_url = browser.find_element_by_xpath(self.audioxpath).get_attribute('src')
        browser.close()
        # TODO
        # TODO check for last episode, if it exists
        new = False  # assume it isn't new until proven
        try:
            newest = self.entry()[0]
        except IndexError:
            new = True
        if not new:
            if newest.title != ep_title:
                new = True
                # this could certainly be more sofisticated than checking for a match on the most recent.


        return


def main():
    page = 'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/'
    RadioTheatre = OnePlacePodCast(page)
    RadioTheatre.title('Radio Theatre')
    RadioTheatre.description('The Weekly broadcast of the award winning audio dramas '
                             'from Focus on the Family, hosted by OnePlace.com')
    RadioTheatre.id(page)

    return RadioTheatre


if __name__ == '__main__':
    main()
