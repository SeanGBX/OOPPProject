import MySQLdb

class CurrentFood:
    def __init__(self, food, price, calories):
        self.__food = food
        self.__price = price
        self.__calories = calories


    def get_food(self):
        return self.__food

    def set_food(self, food):
        self.__food = food

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_calories(self):
        return self.__calories

    def set_calories(self, calories):
        self.__calories = calories

    def insert_food(self):
        connection = MySQLdb.connect(host ='localhost',user = 'root', password = '123admin123',db = 'registerdb')
        cur = connection.cursor()
        cur.execute("INSERT INTO currentfoodlist(food, price, calories) VALUES(%s, %s, %s)", (self.get_food(), self.get_price(), self.get_calories()))
        connection.commit()
        connection.close()

    def __str__(self):
        s = f"{ self.get_food() } has { self.get_calories() } and costs { self.get_price() }"
        return s