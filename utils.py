import json
import re
from MyDatabase import MyDatabase
import urllib.request, json
import threading

# Classe Utils regroupant toutes les methodes de formatage et d'insertion dans la base de donnée
class Utils:

	# Methode permettant d'insérer de la donnée dans la base de donnée en se faisant formater dans un dictionnaire Python (en TwitterStatusInformations)
    def insertDataIntoTheDataBase(status):

    	# On crée un objet TwitterStatusInformations et on insère toute l'information à l'intérieur
        formatedJson = TwitterStatusInformations()
        formatedJson.getInfosFromTwitterStatus(status)

        # On récupère le dictionnaire ainsi crée sous forme d'une chaine de caractère.
        formatedString = formatedJson.getFormatedStringToSendToDatabase()

        try:

        	# Si la tentative de faire une String formatée n'a pas échouée alors on insère la donnée dans la table "bgpstream"
            if formatedString != None:
                MyDatabase.mydb.insert("bgpstream", formatedString)

                # Ici on veut faire ce que nous a demandé Mr Salamatian pour récupérer les adresses des prefixes ainsi que leur description... Mais il y a un soucis... (peut etre lié aux threads)
                if (formatedJson.type == "OT"):

                	# On utilise un thread pour ne pas être bloqué ici... Mais il y a un soucis et on a abandonné car le script s'arrête sans raison.
                    #x = threading.Thread(target=Utils.processBGPPrefixData, args=(formatedJson.idAS,MyDatabase.mydb,))
                    #x.start()
                    pass
        except:
            pass

    # Méthode permettant le processus de traitement pour la recherche de prefixes et d'IPs
    def processBGPPrefixData(idAs, db):
        url = "https://api.bgpview.io/asn/" + re.sub("AS", "", idAs) + "/prefixes"

        # Methode pour récupérer les donnée formatées en JSON depuis le site web
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())

            # Maintenant que nous avons toutes les IP V4 des préfixes en un seul json 
            prefixeList = data.get('data').get('ipv4_prefixes')

            #On insère la donnée, mais il surgit de façon très régulière une erreur inconnue.

            thestr = {"idAS":idAs, "json":prefixeList}
            try:
                db.insert("ipv4_prefixes", thestr)
            except:
                print("MySQL random problem... Danm it I hate Python !")


# Classe nous permlettant de formatter les donnée récupérées dans les Tweets
class TwitterStatusInformations:

	# Le constructeur avec toutes les différents champs
    def __init__(self):
        self.idEvent = None
        self.type = None
        self.country = None
        self.nbPrefix = None
        self.idASHS = None
        self.idAS = None
        self.prefix = None
        self.name = None
        self.timestamp = None

    # C'est ici que toute la magie se passe avec un tweet...
    def getInfosFromTwitterStatus(self, twitterStatus):

    	# Il faut déjà récupérer le JSON et on le coupe pour avoir les différentes parties du tweet (On on aura le type, les prefixes ect)
        string = twitterStatus._json.get('text')
        string = re.sub(r'[,]+', ',', string)

        # Le seul soucis c'est qu'on aura pas tout le temps des tweets "bien formés" avec le bon nombre de virgules donc ça nous pose problème et certains tweets ne seront pas traités...
        stringSplited = string.split(",")

        # On obtient déjà le type du tweet qui nous permettra de choisir quels informations rentrer dans la base de donnée.
        self.type = stringSplited[1]

        # On obtient la date a laquelle le Tweet a été crée pour avoir un ordre de tri
        self.timestamp = twitterStatus._json.get("created_at")

        try:

        	# Si le type est du Hijack (pas desoin de décrire chaques actions car les noms sont explicites)
            if (self.type == 'HJ'):

                self.idAS = stringSplited[2].split(" ")[2]
                self.prefix = stringSplited[2].split(" ")[3]

                if stringSplited[3] != ' ':
                    self.name = stringSplited[3]

                # Nous utilisons la ligneId pour vérifier si la ligne est un code de pays ou un tiret ou un mot Inc.
                lineId = 4

                if stringSplited[4] == ' Inc.':
                    lineId += 1 # S'il y a un Inc. écrit, on "saute" cette ligne

                # C'est la ligne où le code du pays est supposé être, si len est de 3 ça signifie que la balise est un pays et puis nous l'ajoutons
                if len(stringSplited[lineId]) == 3:
                    self.country = re.sub(r'[ ]', '', stringSplited[lineId])
                # Sinon, ça veut dire qu'on a soit un tiret, soit un blanc, donc on ne fait rien

                # Ici on recoupe le texte car des fois il y avait des virgules en trop, et on traite plusieurs cas
                stringSplited = stringSplited[- (len(stringSplited) - lineId):]


                if(stringSplited[0] == '-'):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                if(len(stringSplited[0]) == 3):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                if (stringSplited[0] == '-'):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                self.idASHS = stringSplited[0].split(" ")[1]

                # Ici on veut avoir l'id du Hijack (car l'url est de la forme bgpstream.com/event/IDEvent)
                for ii in twitterStatus._json['entities']['urls']:
                    self.idEvent = ii['display_url']
                    self.idEvent = re.sub(r'(bgpstream.com/event/)', '', self.idEvent)

                    if not self.idEvent.isdigit():
                        self.idEvent = None

            # Maintenant c'est au tour des Outages (ici aussi pas besoin de détailler car les noms son explicites)
            else:

                #Si ce n'est pas un ID, on passe parce que c'est inutile
                if(not stringSplited[2].isdigit()):
                    return

                self.idAS = stringSplited[2]

                if(stringSplited[3] == '-' or stringSplited[3] == '--No Registry Entry--'):
                    return

                self.name = stringSplited[3]

                if(len(stringSplited[4]) > 3):
                    return

                self.country = re.sub(r'[ ]', '', stringSplited[4])

                self.nbPrefix = stringSplited[6].split(" ")[2]

                for ii in twitterStatus._json['entities']['urls']:
                    self.idEvent = ii['display_url']
                    self.idEvent = re.sub(r'(bgpstream.com/event/)', '', self.idEvent)

                    if not self.idEvent.isdigit():
                        self.idEvent = None
        except:
            # print("[IGNORE] Data Bad Format Error...")
            pass

    # Format dictionnaire Python
    def getFormatedStringToSendToDatabase(self):

        if (self.idEvent != None): #and len(self.country) == 2):

            string = {
                "idEvent" : self.idEvent,
                "type" : self.type,
                "country" : self.country,
                "nbPrefix" : self.nbPrefix,
                "idASHS" : self.idASHS,
                "idAS" : self.idAS,
                "prefix" : self.prefix,
                "name" : self.name,
                "timestamp" : self.timestamp
            }

            return string
        else:
            return None