import OneFeed
import pickle

feeds = []

# dictionary for RadioTheatre:

desc = 'The Weekly broadcast of the award winning audio dramas ' \
       'from Focus on the Family, hosted by OnePlace.com'

RTparams = {
    'feed_title': 'Radio Theatre',
    'feed_link': 'http://momentumv.github.io/Onefeed/RadioTheatre.xml',
    'copyright': 'Focus on the Family',
    'feed_desc': desc,
    'feed_image_url': 'https://momentumv.github.io/Onefeed/Files/RT.jpg',
    'feed_author': 'Focus on the Family',
    'feed_owner': 'Focus on the Family',
    'feed_email': 'help@FocusontheFamily.com',
    'feed_summary': desc,
    'items_string': '',
    'page': 'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/'
}
RT = OnePlacePodCast(RTparams)
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-01-of-09'
    '-792544.html')
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-02-of-09'
    '-792545.html')
RT.refresh()
feeds.append(RT)

# dictionary for Turning Point:
desc = 'Dr. David Jeremiah\'s Turning Point Delivers the Unchanging Word of God to an Ever-Changing World'

TPparams = {
    'feed_title': 'Turning Point',
    'feed_link': 'http://momentumv.github.io/Onefeed/TurningPoint.xml',
    'copyright': 'Focus on the Family',
    'feed_desc': desc,
    'feed_image_url': 'https://momentumv.github.io/Onefeed/Files/RT.jpg',
    'feed_author': 'David Jeremiah',
    'feed_owner': 'David Jeremiah',
    'feed_email': 'info@davidjeremiah.org',
    'feed_summary': desc,
    'items_string': '',
    'page': 'https://www.oneplace.com/ministries/turning-point/'
}
TP = OnePlacePodCast(TPparams)

title = 'Turning Point'
author_dict = {'name': 'David Jeremiah', 'email': 'info@davidjeremiah.org'}
TP = OneFeed.OnePlacePodCast(page, title, desc, feed_id)
TP.author(author_dict)
TP.limit = 30
TP.refresh()
feeds.append(TP)

with open('feeds.p', 'wb') as file:
    pickle.dump(feeds, file)
