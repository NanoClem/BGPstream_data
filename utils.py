import json

import re

from MyDatabase import MyDatabase

import urllib.request, json
import threading


class Utils:

    def insertDataIntoTheDataBase(status):
        formatedJson = TwitterStatusInformations()
        formatedJson.getInfosFromTwitterStatus(status)

        # Send the formated string to the database

        formatedString = formatedJson.getFormatedStringToSendToDatabase()

        try:
            if formatedString != None:
                MyDatabase.mydb.insert("bgpstream", formatedString)

                if (formatedJson.type == "OT"):

                    #We use a threah not to be stuck here
                    x = threading.Thread(target=Utils.processBGPPrefixData, args=(formatedJson.idAS,))
                    x.start()
        except:
            pass

    def processBGPPrefixData(idAs):
        url = "https://api.bgpview.io/asn/" + re.sub("AS", "", idAs) + "/prefixes"

        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())

            #Now we have all the ip v4 prefixes in one json we can work...
            prefixeList = data.get('data').get('ipv4_prefixes')

            #If the data alread exists it doesnt matter it wont be added

            thestr = {"idAS":idAs, "json":prefixeList}

            MyDatabase.insert('ipv4_prefixes', thestr)



class TwitterStatusInformations:

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

    def getInfosFromTwitterStatus(self, twitterStatus):
        string = twitterStatus._json.get('text')
        string = re.sub(r'[,]+', ',', string)
        stringSplited = string.split(",")

        self.type = stringSplited[1]
        self.timestamp = twitterStatus._json.get("created_at")

        try:

            if (self.type == 'HJ'):

                self.idAS = stringSplited[2].split(" ")[2]
                self.prefix = stringSplited[2].split(" ")[3]

                if stringSplited[3] != ' ':
                    self.name = stringSplited[3]


                #We use the lineId to check if the line is a country code or a dash or a Inc. word written
                lineId = 4

                if stringSplited[4] == ' Inc.':
                    lineId += 1 #If there is a Inc. written we "jump" this line

                #This is the line where the Country code is suposed to be, if the len if 3 this means the tag is a country and then we add it
                if len(stringSplited[lineId]) == 3:
                    self.country = re.sub(r'[ ]', '', stringSplited[lineId])
                #Else this means we have either a dash or a blank, thus we do nothing

                stringSplited = stringSplited[- (len(stringSplited) - lineId):]


                if(stringSplited[0] == '-'):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                if(len(stringSplited[0]) == 3):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                if (stringSplited[0] == '-'):
                    stringSplited = stringSplited[- (len(stringSplited) - 1):]


                self.idASHS = stringSplited[0].split(" ")[1]

                for ii in twitterStatus._json['entities']['urls']:
                    self.idEvent = ii['display_url']
                    self.idEvent = re.sub(r'(bgpstream.com/event/)', '', self.idEvent)

                    if not self.idEvent.isdigit():
                        self.idEvent = None
            else:

                #If this is not an Id we pass because it is useless
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

            #print(self.idEvent,self.type,self.country,self.nbPrefix,self.idASHS,self.idAS,self.prefix,self.name)
        except:
            print("[IGNORE] Data Bad Format Error...")

    def getFormatedStringToSendToDatabase(self):

        if (self.idEvent != None): #and len(self.country) == 2):

            #print(self.name)

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