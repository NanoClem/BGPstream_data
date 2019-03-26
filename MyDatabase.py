import mysql.connector as mysql


class MyDatabase :
    """
    Cette classe représente un DOM mysql en python de manière a
    pouvoir effectuer les traitements de base sur une BDD
    """

    def __init__(self, _host = "localhost", _user="root", _password="root", _port="3306") :
        """
        CONSTRUCTEUR de la classe MyDatabase
        ATTRIBUTE host : nom d'hote de la bdd
        ATTRIBUTE user : nom d'utilisateur
        ATTRIBUTE password : mot de passe
        ATTRIBUTE mydb : objet PDO
        """
        self.host     = _host
        self.user     = _user
        self.password = _password
        self.port     = _port
        self.mydb     = None



    def connectToMySQL(self) :
        """
        Connexion au domaine mysql
        """
        self.mydb = mysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            passwd = self.password
        )



    def exists(self, DBname) :
        """
        Permet de savoir si une base de donnee existe
        grace au nom passe en parametre
        PARAM DBname : nom de la BDD que l'on cherche
        RETURN : vrai si elle exite, faux sinon
        RETURN TYPE : boolean
        """
        ret = False
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW DATABASES")

        databases = mycursor.fetchall()         # liste de toutes les bdd existantes
        for db in databases :
            if db[0] == DBname :
                ret = True
                break

        return ret



    def formatInsert(self, columns = []) :
        """
        Formatage str pour la requete d'insertion de donnees
        """
        ret = []
        strCol = ""
        strVal = ""
        #FORMATAGE DES COLONNES ET DE LA PARTIE "VALUES"
        for c in columns :
            strCol += c
            strVal += "%s"
            if c != list(columns)[-1] :     # si on ne traite pas la derniere colonne
                strCol += ","
                strVal += ","

        ret.append(strCol)
        ret.append(strVal)
        return ret




    def connectToDB(self, DBname) :
        """
        Connexion a la base de donnee
        passee en parametre
        PARAM DBname : nom de la bdd
        """
        self.mydb = mysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            passwd = self.password,
            database = DBname
        )
        print("Successfuly connected to database %s \n" %DBname)



    def createDatabase(self, DBname) :
        """
        Creation d'une nouvelle base de donnees
        Si la bdd existe deja, affiche un message d'erreur
        PARAM DBname : nom de la bdd a creer
        """
        mycursor = self.mydb.cursor()
        if self.exists(DBname) :
            print("ERROR : Database already existing")
        else :
            mycursor.execute("CREATE DATABASE " + DBname)
            print("Successfuly created database %s" %DBname)



    def createTable(self, tableName, cols = {}) :
        """
        Creation d'une nouvelle table dans
        la bdd courrante
        PARAM tableName : nom de la table a creer
        PARAM cols : informations sur les colonnes de la table (nom/type)
        """
        mycursor = self.mydb.cursor()
        query  = ""
        for key,value in cols.items() :
            query += key + " " + str(value)
            if key != list(cols.keys())[-1] :     #derniere colonne du dicionnaire
                query += ", "

        print("CREATE TABLE %s (%s)" %(tableName,query))
        mycursor.execute("CREATE TABLE %s (%s)" %(tableName,query))
        print("Successfuly created table %s" %tableName)



    def insert(self, tableName, toInsert = {}) :
        """
        Insertion d'une ligne dans la table
        PARAM tableName : nom de la table
        PARAM toInsert : description des donnees a inserer
        """
        mycursor = self.mydb.cursor()
        val     = ()                                    # valeurs a inserer
        format  = self.formatInsert(toInsert.keys())    # mise en forme str de la requete
        columns = format[0]                             # colonnes concernees par l'insertion
        STRval  = format[1]                             # formatage str de la partie "VALUES"

        # DONNEES A INSERER
        for key,value in toInsert.items() :
            val     += (str(value),)

        query = "INSERT INTO " + tableName + "(" + columns + ")" + " VALUES(" + STRval + ")"   # attention : pas generique
        mycursor.execute(query, val)
        self.mydb.commit()



    def insertMultiple(self, tableName, toInsert = []) :
        """
        Meme principe que la fontion insert(),
        mais pour l'insertion multiple
        PARAM tableName : nom de la table
        PARAM toInsert : description des donnees a inserer
        """
        mycursor = self.mydb.cursor()
        vals    = []                                            # valeurs a inserer
        dataVal = ()
        format  = self.formatInsert(list(toInsert[0].keys()))   # mise en forme str de la requete
        columns = format[0]                                     # colonnes concernees par l'insertion
        STRval  = format[1]                                     # formatage str de la partie "VALUES"

        # DONNEES A INSERER
        for data in toInsert :
            for key,value in data.items() :
                dataVal += (str(value),)        # recuperation des donnes a inserer
            vals.append(dataVal)                # ajout dans la liste des valeurs
            dataVal = ()

        query = "INSERT INTO " + tableName + "(" + columns + ")" + " VALUES(" + STRval + ")"
        mycursor.executemany(query, vals)
        self.mydb.commit()
