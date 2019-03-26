import json

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
        stringSplited = string.split(",")


        self.type = stringSplited[1]

        if(self.type == 'HJ'):
            self.idAS = stringSplited[2].split(" ")[2]
            self.prefix = stringSplited[2].split(" ")[3]
            self.name = stringSplited[3]
            self.country = stringSplited[4]
            self.idASHS = stringSplited[6].split(" ")[1]
            #self.idEvent = stringSplited[7]


        else:
            pass

        print(stringSplited.__len__())
        print(twitterStatus._json.get('text'))
        print(self.idEvent, self.type, self.country, self.nbPrefix, self.idASHS, self.idAS, self.prefix, self.name)