from MyDatabase import MyDatabase



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
    toInsert = {
        "idUser"   : 55545256,
        "pseudo"   : "Kikoo",
        "location" : "France"
    }


    db = MyDatabase()

    #CREATION ET CONNECTION A LA BDD
    db.connectToMySQL()
    db.createDatabase(TwiDatabase)
    db.connectToDB(TwiDatabase)

    #OPERATION SUR LA BDD
    # db.createTable("user", user)
    # db.createTable("tweet", tweet)
    db.insert("User", toInsert)



if __name__ == '__main__':
    main()
