# import os
import shutil
import urllib

import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
# from bs4 import BeautifulSoup
import time
from feedgen.feed import FeedGenerator




class Podcast:
    """
    This class is designed to hold all the details required for generating a podcast.
    It includes a default string to use for the RSS feed.
    It also includes a not implemented method for updating/finding new episodes.
    This should be implemented in whatever subclasses are needed.
    """
    self.feed_text = \
        ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
         "<rss version=\"2.0\" xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" "
         "xmlns:atom=\"http://www.w3.org/2005/Atom\" "
         "xmlns:media=\"http://search.yahoo.com/mrss/\" "
         "xmlns:content=\"http://purl.org/rss/1.0/modules/content/\">\n"
         "<channel>\n"
         "    <atom:link href=\"{self_url}\" rel=\"self\" type=\"application/rss+xml\"/>\n"
         "    <title>{feed_title}</title>\n"
         "    <link>{feed_link}</link>\n"
         "    <copyright>{copyright}</copyright>\n"
         "    <description>\n"
         "        {feed_desc}\n"
         "    </description>\n"
         "    <image>\n"
         "        <url>\n"
         "            {feed_image_url}\n"
         "        </url>\n"
         "        <title>{feed_title}</title>\n"
         "        <link>{feed_link}</link>\n"
         "    </image>\n"
         "    <itunes:image href=\"{feed_image_url}\"/>\n"
         "    <language>en</language>\n"
         "    <itunes:explicit>no</itunes:explicit>\n"
         "    <itunes:category text=\"{feed_category}\">\n"
         "        <itunes:category text=\"{feed_subcategory}\"/>\n"
         "    </itunes:category>\n"
         "    <itunes:author>{feed_author}</itunes:author>\n"
         "    <itunes:owner>\n"
         "        <itunes:name>{feed_owner}</itunes:name>\n"
         "        <itunes:email>{feed_email}</itunes:email>\n"
         "    </itunes:owner>\n"
         "    <itunes:summary>{feed_summary}\n"
         "    </itunes:summary>\n"
         "    <lastBuildDate>{feed_build}</lastBuildDate>\n"
         " {items_string}\n"
         "    </channel>\n"
         "</rss>")

    class Entry:
        """
        A single object that holds all the details needed for a podcast item tag

        """
        item_template = \
            ('<item>\n'
             '      <guid isPermaLink="false"><![CDATA[{guid}]]></guid>\n'
             '      <title>{title}</title>\n'
             '      <description>\n'
             '      {description}\n'
             '      </description>\n'
             '      <itunes:author>{author}\n'
             '      </itunes:author>\n'
             '      <itunes:subtitle/>\n'
             '      <itunes:summary>\n'
             '       {description}\n'
             '      </itunes:summary>\n'
             '      <pubDate>{pubdate}</pubDate>\n'
             '      <enclosure url="{url}" length="0" type="audio/mpeg"/>\n'
             ' </item>')

        def __init__(self):
            self.guid = ''
            self.title = ''
            self.description = ''
            self.author = ''
            self.pubdate = ''
            self.url = ''

        def __repr__(self):
            return self.item_template.format(**vars(self))

    def __init__(self, title=None):
        self.title = 'title'
        pass

    def refresh(self, page=None):
        raise NotImplementedError

    def write_rss(self, filename=None):
        pass


# each "show" has its own object, that gets updater functions added to it
class PodCastOld(FeedGenerator):
    def __init__(self):
        """
        This wrapper of FeedGenerator adds the podcast extension at creation.
        """
        super().__init__()
        self.__download = False  # this is to signal if the podcast should save the file when it updates
        self.load_extension('podcast')
        self.__downloadpath = None

    def get_download(self, both=False):
        if both:
            return {'download': self.__download, 'path': self.__downloadpath}
        else:
            return self.__download

    def set_download(self, download, path=None):
        if download:
            if path is None:
                path = self.__downloadpath
            try:
                assert path is not None
            except AssertionError:
                print('If download is set, a path must be set. Use ".set_download(True, path_as_a_string)"\n'
                      ' Because no path has been given,download is not set.')
                self.__download = False
                return self.__download
            # if there is a path provided, go ahead and set download to true and set the path to the provided string
            self.__download = True
            self.__downloadpath = path
        else:
            self.__download = False
        return {'download': self.__download, 'path': self.__downloadpath}


class OnePlacePodCast(PodCast):
    def __init__(self, page=None, feedtitle=None, feeddesc=None, feedid=None):
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
        self.podcast.itunes_category('Christianity')
        self.pageUrl = page  # this is to be accessible and updated when this class is instanced
        self.titlexpath = '//div[@class="overlay2"]//h2'  # might need customizing for each page?
        self.descxpath = '//div[@class="description"]'
        self.audioxpath = '//audio'
        self.datexpath = '//div[@class="overlay2"]//div[@class="liveDate"]'
        # the pageUrl should be the url to be retrieved during updating.
        self.limit = 6

    def rss_file(self, filename):
        fields = dict(self_url=None,
                      feed_title=None,
                      feed_link=None,
                      copyright=None,
                      feed_desc=None,
                      feed_image_url=None,
                      feed_category=None,
                      feed_subcategory=None,
                      feed_author=None,
                      feed_owner=None,
                      feed_email=None,
                      feed_summary=feed_desc,
                      feed_build=datetime.now().strftime(
                          "%a, %d %b %Y %H:%M:%S") + ' +0000')  # Mon, 20 Jan 2020 19:25:57 +0000
        with open('template_feed_head.xml', 'r') as f:
            template = f.read()
        with open('template_item.xml', 'r') as f:
            item_text = f.read()
        with open(f'{selflink}', 'w') as rss:
            rss.write(template.format(**fields))
        with open(f'{selflink}', 'a') as rss:
            for e in self.entry():
                rss.write(item_text.format(**ep_fields))

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
        ep_date = browser.find_element_by_xpath(self.datexpath).text
        browser.close()
        new = False  # assume it isn't new until proven
        try:
            newest = self.entry()[0]
        except IndexError:
            # if the list has no elements, then any episode is a 'new' episode
            new = True
        if not new:
            # check to see if the episode is the same as the last one. If so, don't add it again!
            if newest.title() == ep_title:
                return None
                # this could certainly be more sophisticated than checking for a match on the most recent,
                # but this is probably good enough.
            else:
                new = True
        assert new
        ep = self.add_entry()
        ep.id(str(hash(ep_url)))
        ep.title(ep_title)
        ep.description(ep_description)
        ep.enclosure(ep_url, 0, 'audio/mpeg')
        ep.pubDate(ep_date)
        if self.get_download():
            filename = '\\'.join([self.get_download(both=True)['path'], ep_title])
            filename = filename + '.' + ep_url.split('.')[-1]
            url = ep_url
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        # respect episode count limit
        while 0 < self.limit < len(self.entry()):
            self.remove_entry(self.entry()[-1])
        return ep
