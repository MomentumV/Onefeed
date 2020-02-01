# TODO create a version updater that scrapes the properties of the pickled feeds and recreates them with the most recent Onefeed edit.
import pickle
import OneFeed
#pickle import
with open('feeds.p','rb') as file:
    feeds=pickle.load(file)

# iterate through feeds, then items, creating new versions

for f in feeds:
    #make a new feed
    new = OneFeed.

    pass