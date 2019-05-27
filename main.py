from MyDatabase import MyDatabase

from twitter import TwitterAPI
from twitter import StreamListener
from utils import Utils

import threading

def main() :

	# On utilise MyDatabase.mydb de manière statique et non un objet
    MyDatabase.mydb = MyDatabase("localhost", "root", "", "3306", "proj632_project1")

    # Connection à la base de donnée
    MyDatabase.mydb.connectToMySQL()

    #The BGP Stream part using the search method

    # On crée un objet twitterAPI qui sera l'API twitter utilisée plus loin
    twitterAPI = TwitterAPI()

    # Le stream listener utilisé pour "écouter" le compte de BGP Stream
    streamListener = StreamListener()

    # Ici nous voulions utilisé la méthode de stream pour "écouter" le compte de BGP Stream (c'est son Id dans la String) et récupérer les tweets pour les traiter.
    # On utilise un thread pour taiter cette méthode et pour traiter les tweets précédement envoyés par BGP Stream
    x = threading.Thread(target=streamListener.useStreamByUser, args=(twitterAPI,'3237083798'))
    x.start()

    # On laisse le thread crée précédement tourner de son coté pendant que l'on traite les anciens tweets.
    twitterAPI.getAllTweetsFromUser('bgpstream')

if __name__ == '__main__':
    main()