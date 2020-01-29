# import os
import shutil
import hashlib

import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
# from bs4 import BeautifulSoup
import time
from datetime import datetime


class PodCast:
    """
    This class is designed to hold all the details required for generating a podcast.
    It includes a default string to use for the RSS feed.
    It also includes a not implemented method for updating/finding new episodes.
    This should be implemented in whatever subclasses are needed.
    """
    feed_text = \
        ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
         "<rss version=\"2.0\" xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" "
         "xmlns:atom=\"http://www.w3.org/2005/Atom\" "
         "xmlns:media=\"http://search.yahoo.com/mrss/\" "
         "xmlns:content=\"http://purl.org/rss/1.0/modules/content/\">\n"
         "<channel>\n"
         "    <atom:link href=\"{self_link}\" rel=\"self\" type=\"application/rss+xml\"/>\n"
         "    <title>{feed_title}</title>\n"
         "    <link>{page}</link>\n"
         "    <copyright>{copyright}</copyright>\n"
         "    <description>\n"
         "        {feed_desc}\n"
         "    </description>\n"
         "    <image>\n"
         "        <url>\n"
         "            {feed_image_url}\n"
         "        </url>\n"
         "        <title>{feed_title}</title>\n"
         "        <link>{page}</link>\n"
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

    def __init__(self, *initial_data, **kwargs):
        """

        :param initial_data:
         one or more dictionaries with the following fields:
            {
            feed_title : ''
            feed_link : ''
            copyright : ''
            feed_desc : ''
            feed_image_url : ''
            feed_category : ''
            feed_subcategory : ''
            feed_author : ''
            feed_owner : ''
            feed_email : ''
            feed_summary : ''
            feed_build : ''
            items_string : ''
            }

        :param kwargs:
            Any of the dictionary fields, but also
            download
            download_path

        """
        self.download = False
        self.download_path = None
        self.limit = 0
        empty_dict = {
            'feed_title': '',
            'self_link': '',
            'page': '',
            'copyright': '',
            'feed_desc': '',
            'feed_image_url': '',
            'feed_category': '',
            'feed_subcategory': '',
            'feed_author': '',
            'feed_owner': '',
            'feed_email': '',
            'feed_summary': '',
            'feed_build': '',
            'items_string': ''
        }
        # populate empty parameters
        for key in empty_dict:
            setattr(self, key, empty_dict[key])
        # populate parameters from passed in dictionary
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        # populate parameters from keywords passed in
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.entries = []

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

        def __str__(self):
            return self.item_template.format(**vars(self))

        def __repr__(self):
            return str(type(self))

    def refresh(self, page=None):
        raise NotImplementedError

    def write_rss(self, filename=None):
        self.items_string = '\n'.join([str(e) for e in self.entries])
        self.feed_build = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")  # Mon, 20 Jan 2020 19:25:57 GMT
        if filename is not None:
            with open(filename, 'w') as outfile:
                outfile.write(str(self))
        else:
            print(self)
        pass

    def __repr__(self):
        return str(vars(self))

    def __str__(self):
        return self.feed_text.format(**vars(self))


class OnePlacePodCast(PodCast):
    def __init__(self, *dicts, **kwargs):
        """
        docstring TODO yeah
        """
        self.page = None
        super().__init__(*dicts, **kwargs)
        self.feed_category = 'Religion &amp; Spirituality'
        self.feed_subcategory = 'Christianity'
        self.titlexpath = '//div[@class="overlay2"]//h2'  # might need customizing for each page?
        self.descxpath = '//div[@class="description"]'
        self.audioxpath = '//audio'
        self.datexpath = '//div[@class="overlay2"]//div[@class="liveDate"]'

    def refresh(self, page=None):
        """
        Starts a headless Firefox browser to load the page and render and navigate the source.
        :return:
        """
        if page is None and self.page is not None:
            page = self.page
        # would be good to do some regex checking on page passed in
        # Firefox headless browser
        opts = Options()
        opts.headless = True
        assert opts.headless  # Operating in headless mode
        browser = Firefox(options=opts)
        browser.get(page)
        time.sleep(4)  # wait for page to load and render
        ep_title = browser.find_element_by_xpath(self.titlexpath).text
        ep_description = browser.find_element_by_xpath(self.descxpath).text.encode('ascii',
                                                                                   'xmlcharrefreplace').decode()
        ep_url = browser.find_element_by_xpath(self.audioxpath).get_attribute('src')
        ep_date_text = browser.find_element_by_xpath(self.datexpath).text
        ep_date = datetime.strptime(ep_date_text, '%B %d, %Y').strftime("%a, %d %b %Y %H:%M:%S GMT")
        browser.close()
        new = False  # assume it isn't new until proven
        try:
            newest = self.entries[0]
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
        ep = self.Entry()
        m = hashlib.md5()
        m.update(ep.url.encode())
        ep.guid = m.hexdigest()
        ep.title = ep_title
        ep.description = ep_description
        ep.author = self.feed_author
        ep.pubdate = ep_date
        ep.url = ep_url
        self.entries = [ep] + self.entries
        if self.download:
            filename = '\\'.join([self.download_path, ep_title])
            filename = filename + '.' + ep_url.split('.')[-1]
            url = ep_url
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        # respect episode count limit
        while 0 < self.limit < len(self.entries):
            self.entries.pop()
        return ep
