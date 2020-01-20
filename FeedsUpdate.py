
import pickle
import git_code
with open('feeds.p', 'rb') as f:
    feeds = pickle.load(f)

# call the refresh of each feed and then write the rss feed
with open('update.log', 'w') as log:
    for feed in feeds:
        try:
            ep = feed.refresh()
        except:
            log.write(f'exception updating {feed.title()}')
        if ep is None:
            log.write(f'No new show for {feed.title()}')
        else:
            log.write(f'{ep.title()} added to {feed.title()}')
            # write out the rss file if there is an episode added
            feed.rss_file()

    # the refresh wil download any flagged as such.
# re-pickle the feeds file:
with open('feeds.p', 'wb') as file:
    pickle.dump(feeds, file)
# commit the project folder and push to github
git_code.git_push()
