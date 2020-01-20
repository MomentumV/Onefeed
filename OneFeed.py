# import os
import shutil
import urllib

import requests
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
        self.downloadpath = None

    def set_download(self, download=False, path=None):
        if download:
            if path is None:
                path = self.downloadpath
            try:
                assert path is not None
            except AssertionError:
                print('If download is set, a path must be set. Use ".set_download(True, pathasastring)"\n'
                      ' Because no path has been given,download is not set.')
                self.__download = False
                return self.__download
            # if there is a path provided, go ahead and set download to true
            self.__download = True
        else:
            self.__download = False
        return self.__download


class OnePlacePodCast(PodCast):
    def __init__(self, page=None, feedtitle=None,feeddesc=None,feedid=None):
        """
        a wrapper around the PodCast init(), which adds a few OnePlace specific details, and the
        xpaths needed for the extraction of episode details
        :param page: the url that is fetched during update
        """
        super().__init__()
        if feedtitle is not None:
            self.title(feedtitle)
        if feeddesc is not None:
            self.description(feeddesc)
        if feedid is not None:
            self.id(feedid)
        else:
            self.id(page)
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
            filename = urllib.parse.quote_plus(self.title())+'+rss.xml'
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
        ep.id(hash(ep_url))
        ep.title(ep_title)
        ep.description(ep_description)
        ep.enclosure(ep_url, 0, 'audio/mpeg')
        if self.set_download():
            filename = '\\'.join([self.downloadpath,ep_title])
            filename = filename + ep_url.split('.')[-1]
            url = ep_url
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        # respect episode count limit
        while 0 < self.limit < len(self.entry()):
            self.remove_entry(self.entry()[-1])
        return ep