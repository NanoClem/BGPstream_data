import json

import tweepy
from utils import Utils


class TwitterAPI:

    def __init__(self):
        # user credentials to access Twitter API
        access_token = "1090251522473160705-sA7oi1AIiNTNJUl2A2PjGngijy44vy"
        access_secret = "qzIJ66jtiyxKHB0zwBhiifKSL4c9RLj2LGaHevnr92BuV"
        consumer_key = "dspktk1iXqA2yYHBrVkncPQw9"
        consumer_secret = "F323o3PI0UrO9ZvB4WWKx21QV3zxp1RrRF4aY4Rj1DR3beJCeL"

        # Setup tweepy to authenticate with Twitter credentials:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        # Create the api to connect to twitter with your creadentials
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    def getAPI(self):
        return self.api

    def getAllTweetsFromUser(self, user, db):
        for tweet in tweepy.Cursor(self.getAPI().user_timeline, id=user).items():

            """
            
            formatedJson = TwitterStatusInformations()
            formatedJson.getInfosFromTwitterStatus(tweet)

            #Send the formated string to the database

            formatedString = formatedJson.getFormatedStringToSendToDatabase()


            try:
                if formatedString != None:
                    db.insert("bgpstream", formatedString)
            except:
                pass
            """

            Utils.insertDataIntoTheDataBase(tweet)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        Utils.insertDataIntoTheDataBase(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def useStreamByUser(self, twitterAPI, userid):
        tweetStream = tweepy.Stream(auth=twitterAPI.getAPI().auth, listener=self)
        tweetStream.filter(follow=[userid])

    def useStreamByWords(self, twitterAPI, words):
        tweetStream = tweepy.Stream(auth=twitterAPI.getAPI().auth, listener=self)
        tweetStream.filter(track=words)

# 3237083798 is The id of bgpstream
# 1090251522473160705 isthe Id of the Missy Project