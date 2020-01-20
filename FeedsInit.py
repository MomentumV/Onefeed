import OneFeed
import pickle

feeds = []

page = 'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/'
title = 'Radio Theatre'
desc = 'The Weekly broadcast of the award winning audio dramas ' \
       'from Focus on the Family, hosted by OnePlace.com'
author_dict = {'name': 'Focus on the Family', 'email': 'help@FocusontheFamily.com'}
feed_id = page
RT = OneFeed.OnePlacePodCast(page, title, desc, feed_id)
RT.author(author_dict)
RT.set_download(True, 'E:\\Audio Theatre and Drama\\OnePlace - Radio Theatre')
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-01-of-09'
    '-792544.html')
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-02-of-09'
    '-792545.html')
RT.refresh()
feeds.append(RT)

page = 'https://www.oneplace.com/ministries/turning-point/'
title = 'Turning Point'
desc = 'Dr. David Jeremiah\'s Turning Point Delivers the Unchanging Word of God to an Ever-Changing World'
feed_id = page
author_dict = {'name': 'David Jeremiah', 'email': 'info@davidjeremiah.org'}
TP = OneFeed.OnePlacePodCast(page, title, desc, feed_id)
TP.author(author_dict)
TP.limit = 30
TP.refresh()
feeds.append(TP)

with open('feeds.p', 'wb') as file:
    pickle.dump(feeds, file)
