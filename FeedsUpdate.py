
import pickle
import git_code
from datetime import datetime
with open('feeds.p', 'rb') as f:
    feeds = pickle.load(f)

# call the refresh of each feed and then write the rss feed
with open('update.log', 'a') as log:
    for feed in feeds:
        try:
            ep = feed.refresh()
        except:
            log.write(str(datetime.now()))
            log.write(f':\texception updating {feed.title()}\n')
        if ep is None:
            log.write(f':\tNo new show for {feed.title()}\n')
        else:
            log.write(f':\t{ep.title()} added to {feed.title()}')
            # write out the rss file if there is an episode added
            feed.rss_file()

    # the refresh wil download any flagged as such.
# re-pickle the feeds file:
with open('feeds.p', 'wb') as file:
    pickle.dump(feeds, file)
# commit the project folder and push to github
git_code.git_push()
