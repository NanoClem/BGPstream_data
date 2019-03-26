import json

import re

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

    def getInfosFromTwitterStatus(self, twitterStatus):
        string = twitterStatus._json.get('text')
        string = re.sub(r'[,]+', ',', string)
        stringSplited = string.split(",")


        """

        self.type = stringSplited[1]

        i = 2;

        if(self.type == 'HJ'):
            self.idAS = stringSplited[i].split(" ")[2]
            self.prefix = stringSplited[i].split(" ")[3]

            i+=1;

            self.name = stringSplited[i]

            if (stringSplited[i] == " Inc."):
                i+=1

            if (stringSplited[i] != "-"):
                self.country = stringSplited[i]

            i += 1

            if (stringSplited[i] == "-"):
                i += 1

            self.idASHS = stringSplited[i].split(" ")[1]

            i+=1

            for ii in twitterStatus._json['entities']['urls']:
                self.idEvent = ii['display_url']
                self.idEvent = re.sub(r'(bgpstream.com/event/)', '', self.idEvent)

                if not self.idEvent.isdigit():
                    self.idEvent = None
        else:


            self.idAS = stringSplited[i]

            i+=1

            self.name = stringSplited[i]

            i+=1

            self.country = stringSplited[i]

            i+=1

            if stringSplited[i] == '-':
                i+=1


            try:
                self.nbPrefix = stringSplited[i].split(" ")[2]
            except:
                pass

            for ii in twitterStatus._json['entities']['urls']:
                self.idEvent = ii['display_url']
                self.idEvent = re.sub(r'(bgpstream.com/event/)', '', self.idEvent)

                if not self.idEvent.isdigit():
                    self.idEvent = None

        self.country = re.sub(r'[ ]*', '', self.country)

        """

        self.type = stringSplited[1]

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


    def getFormatedStringToSendToDatabase(self):

        if (self.idEvent != None): #and len(self.country) == 2):

            print(self.name)

            string = {
                "idEvent" : self.idEvent,
                "type" : self.type,
                "country" : self.country,
                "nbPrefix" : self.nbPrefix,
                "idASHS" : self.idASHS,
                "idAS" : self.idAS,
                "prefix" : self.prefix,
                "name" : self.name
            }

            return string
        else:
            return None