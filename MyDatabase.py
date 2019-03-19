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
        print("Successfuly connected to database %s" %DBname)



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
        val     = ()                            # valeurs a inserer
        STRval  = ""                            # mise en forme str de la patie "VALUES" de la requete
        columns = ""                            # colonnes concernees par l'insertion
        for key,value in toInsert.items() :
            columns += key
            val     += (str(value),)
            STRval  += "%s"
            if key != list(toInsert.keys())[-1] :   # si on est pos en fin de liste
                columns += ", "
                STRval  += ", "

        query = "INSERT INTO " + tableName + "(" + columns + ")" + " VALUES(" + STRval + ")"   # attention : pas generique
        print(query, val)
        mycursor.execute(query, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted")
