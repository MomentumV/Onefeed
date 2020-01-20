
import pickle
from git_code import git_push

# call the refresh of each feed and then write the rss feed
with open('update.log', 'wb') as log:
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
# commit the project folder and push to github
git_push()
