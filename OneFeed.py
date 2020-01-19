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
        self.__download = False  # this property is to signal if the podcast should save the file when it updates
        self.load_extension('podcast')

    def set_download(self, download=False):
        if download:
            self.__download = True
        else:
            self.__download = False
        return self.__download


class OnePlacePodCast(PodCast):
    def __init__(self, page=None, feedtitle=None,feeddesc=None):
        """
        a wrapper around the PodCast init(), which adds a few OnePlace specific details, and the
        xpaths needed for the extraction of episode details
        :param page: the url that is fetched during update
        """
        super().__init__()
        self.link(href='http://oneplace.com', rel='alternate')
        self.language('en')
        self.podcast.itunes_category('Christianity')
        self.pageUrl = page  # this is to be accessible and updated when this class is instanced
        self.titlexpath = '//div[@class="overlay2"]//h2'  # might need customizing for each page?
        self.descxpath = '//div[@class="description"]'
        self.audioxpath = '//audio'
        # the pageUrl should be the url to be retrieved during updating.
        self.limit = 6

    def rss_file(self, filename=None, pretty=True):
        if filename is None:
            filename = self.title()+'_rss.xml'
        extensions = True
        encoding = 'UTF-8'
        xml_declaration = True
        super().rss_file(filename, extensions, pretty, encoding, xml_declaration)

    def refresh(self, page=None):
        """
        Starts a headless Firefox browser to load the page and render the source. That source is passed into
        BeautifulSoup to easily extract the latest link, title, description
        :return:
        """
        if page is None:
            page = self.pageUrl
        # would be good to do some regex checking on page passed in
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        browser = Firefox(options=opts)
        browser.get(page)
        time.sleep(4)
        ep_title = browser.find_element_by_xpath(self.titlexpath).text
        ep_description = browser.find_element_by_xpath(self.descxpath).text
        ep_url = browser.find_element_by_xpath(self.audioxpath).get_attribute('src')
        browser.close()
        new = False  # assume it isn't new until proven
        try:
            newest = self.entry()[0]
        except IndexError:
            # if the list has no elements, then any episode is a 'new' episode
            new = True
        if not new:
            # check to see if the episode is the same as the last one. If so, don't add it again!
            if newest.title == ep_title:
                return None
                # this could certainly be more sophisticated than checking for a match on the most recent,
                # but this is probably good enough.
            else:
                new = True
        assert new
        ep = self.add_entry()
        ep.id(ep_url)
        ep.title(ep_title)
        ep.description(ep_description)
        ep.enclosure(ep_url, 0, 'audio/mpeg')
        # TODO if download flagged, then download it.
        # respect episode count limit
        while self.limit > 0 and self.limit > len(self.entry()):
            self.remove_entry(self.entry()[-1])
        return ep


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
