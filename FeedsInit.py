import OneFeed
import pickle

feeds = []

page = 'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/'
title = 'Radio Theatre'
desc = 'The Weekly broadcast of the award winning audio dramas ' \
       'from Focus on the Family, hosted by OnePlace.com'
id = page
RT = OneFeed.OnePlacePodCast(page, title, desc, id)
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-01-of-09-792544.html')
RT.refresh(
    'https://www.oneplace.com/ministries/focus-on-the-familys-radio-theatre/listen/the-hiding-place-part-02-of-09-792545.html')
RT.refresh()
feeds.append(RT)

page = 'https://www.oneplace.com/ministries/turning-point/'
title = 'Turning Point'
desc = "Dr. David Jeremiah's Turning Point has a Mission: Delivering the Unchanging Word of God to an Ever-Changing " \
       "World "
id = page
TP = OneFeed.OnePlacePodCast(page, title, desc, id)
TP.limit = 30
TP.refresh()
feeds.append(TP)

with open('feeds.p', 'wb') as file:
    pickle.dump(feeds, file)
