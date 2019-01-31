import MySQLdb


class Profile:
    def __init__(self, name, username, email, ID):
        self.name = name
        self.username = username
        self.email = email
        self.ID = ID

    def getName(self):
        return self.name

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getID(self):
        return self.ID

    def setName(self, name):
        self.name = name

    def setUsername(self, username):
        self.username = username

    def setEmail(self, email):
        self.email = email

    def setID(self, ID):
        self.ID = ID

    def changeProfile(self):

        connection = MySQLdb.connect(host='localhost', user='root', password='123admin123', db='registerdb')
        cur = connection.cursor()
        cur.execute("UPDATE users SET name=%s, username=%s, email=%s WHERE id=%s ",
                    (self.getName(), self.getUsername(), self.getEmail(), self.getID()))
        connection.commit()
        connection.close()