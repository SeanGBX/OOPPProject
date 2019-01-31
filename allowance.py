import MySQLdb

class Allowance:
    def __init__(self, weekly):
        self.weekly = weekly

    def getAllowance(self):
        return self.weekly

    def setAllowance(self, weekly):
        self.weekly = weekly

    def changeAllowance(self):
        connection = MySQLdb.connect(host='localhost', user='root', password='123admin123', db='registerdb')
        cur = connection.cursor()
        cur.execute("UPDATE allowance SET weekly=%s", [self.weekly])
        connection.commit()
        connection.close()