import pickle

# load the pickled list of feeds
with open('feeds.p', 'rb') as file:
    feeds = pickle.load(file)

# call the refresh of each feed and then write the rss feed
with open('update.log', 'wb') as log:
    for feed in feeds:
        try:
            ep = feed.refresh()
        except:
            log.write(f'exception updating {feed.title()}')
        if ep is None:
            log.write(f'No new show for {feed.title()}')
        else log.write(f'{ep.title()} added to {feed.title()}')

    #the refresh wil download any flagged as such.
# commit the docs folder and push to github
