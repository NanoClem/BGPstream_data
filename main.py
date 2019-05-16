from MyDatabase import MyDatabase

from twitter import TwitterAPI
from twitter import StreamListener
from utils import Utils

import threading

db = None

def main() :
    #INFORMATIONS SUR LA BDD
    TwiDatabase = "twitterdatabase"
    user = {                                        #description des colonnes
        "idUser"    : "VARCHAR(50) PRIMARY KEY",
        "pseudo"    : "VARCHAR(50)",
        "location"  : "VARCHAR(30)",
        "time_zone" : "VARCHAR(30)"
    }
    tweet = {
        "idTweet"      : "VARCHAR(50) PRIMARY KEY",
        "created_date" : "VARCHAR(30)",
        "content"      : "VARCHAR(280)",
        "hashtags"     : "VARCHAR(30)",
        "geo"          : "VARCHAR(30)",
        "coords"       : "VARCHAR(20)",
        "place"        : "VARCHAR(30)",
        "lang"         : "VARCHAR(20)"
    }

    # DONNEES A INSERER
    #SIMPLE
    userData = {
        "idUser"   : 55545256,
        "pseudo"   : "Kikoo",
        "location" : "France"
    }
    #MULTIPLE
    userTweets = [
        {
            "idTweet" : 4544547,
            "content" : "koukou"
        },
        {
            "idTweet" : 5632548,
            "content" : "c moa"
        }
    ]


    db = MyDatabase("localhost", "root", "", "3306")

    #CREATION ET CONNECTION A LA BDD
    db.connectToMySQL()
    db.createDatabase("proj632_project1")
    db.connectToDB("proj632_project1")

    MyDatabase.mydb = db

    #OPERATION SUR LA BDD
    # db.createTable("user", user)
    # db.createTable("tweet", tweet)
    # db.insert("user", userData)
    # db.insertMultiple("tweet", userTweets)

    #The BGP Stream part using the search method
    twitterAPI = TwitterAPI()
    streamListener = StreamListener()

    #Here we want to use the Stream method and we are puting it into a Thread so it will run by itself while the program is doing things...
    x = threading.Thread(target=streamListener.useStreamByUser, args=(twitterAPI,'3237083798'))
    x.start()

    #While here we gather the old information
    twitterAPI.getAllTweetsFromUser('bgpstream', db)



if __name__ == '__main__':
    main()