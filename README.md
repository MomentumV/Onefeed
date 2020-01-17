# OneFeed README #
 
 ## About ##
 This app uses some basic web scraping with BeautifulSoup to create podcast feed xml files. Its name is a reference
 to OnePlace.com, which hosts many radio programs, but does not provide podcast feeds for many of them.
 
 ## Setup instructions ##
   - This is a Python 3 app.
   - Because this was created with OnePlace in mind, there is little to do with downloading/storing audio files;
   the are linked directly to OnePlace's servers.
   - The FeedGenerator class is subclassed to create a Podcast class that is the foundation for each show this app
   creates. However, each podcast (based on a particular radio program) likely needs its own scraping function customized. 
   This is done by different subclasses of the feedgen FeedGenerator. If you want to use this for other websites, 
   you'll likely want to have a different subclass of the Podcast class.


 ## helpful hints ##
   - none yet