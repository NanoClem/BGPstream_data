import json

import tweepy
from utils import Utils

# La classe Twitter API permettant de nous connecter à l'API twitter
class TwitterAPI:

    def __init__(self):
    	# Données pour accéder à l'API Twitter
        access_token = "1090251522473160705-sA7oi1AIiNTNJUl2A2PjGngijy44vy"
        access_secret = "qzIJ66jtiyxKHB0zwBhiifKSL4c9RLj2LGaHevnr92BuV"
        consumer_key = "dspktk1iXqA2yYHBrVkncPQw9"
        consumer_secret = "F323o3PI0UrO9ZvB4WWKx21QV3zxp1RrRF4aY4Rj1DR3beJCeL"

        # Mise en place de Tweepy pour l'authentification
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        # Crée l'API et nous connecte à Twitter avec nos informations developpeur
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    def getAPI(self):
        return self.api

    # Permet d'avoir tous les tweets (dans la limite de 2300) d'un utilisateur avec son id Twitter
    def getAllTweetsFromUser(self, user):
        for tweet in tweepy.Cursor(self.getAPI().user_timeline, id=user).items():

        	# On insère la donnée dans la base de donnée après l'avoir formatée
            Utils.insertDataIntoTheDataBase(tweet)

# La classe StreamListener étendant de la classe tweepy.StreamListener pour "ecouter en streaming" l'emission de tweets.
class StreamListener(tweepy.StreamListener):

	# A chaques fois qu'une personne tweets quelque chose on le récupère de cette façon
    def on_status(self, status):

    	# On insère la donnée dans la base de donnée après l'avoir formatée
        Utils.insertDataIntoTheDataBase(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    # Methode permettant d'avoir le stream d'un utilisateur par rapport à son id
    def useStreamByUser(self, twitterAPI, userid):
        tweetStream = tweepy.Stream(auth=twitterAPI.getAPI().auth, listener=self)
        tweetStream.filter(follow=[userid])

    # Methode permettant d'avoir le stream d'un ou plusieurs mot(s) clef(s)
    def useStreamByWords(self, twitterAPI, words):
        tweetStream = tweepy.Stream(auth=twitterAPI.getAPI().auth, listener=self)
        tweetStream.filter(track=words)

# 3237083798 is The id of bgpstream
# 1090251522473160705 isthe Id of the Missy Project