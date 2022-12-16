from DatabaseSingletone import DatabaseSingleton
import psycopg2


class Database(metaclass=DatabaseSingleton):

    def __init__(self):
        self.__connection = psycopg2.connect("dbname='SkillPlant' host='localhost' user='postgres' password='changeme'")

    def getConnection(self):
        return self.__connection

