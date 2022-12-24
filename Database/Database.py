from DatabaseSingletone import DatabaseSingleton
import psycopg2


class Database(metaclass=DatabaseSingleton):

    def __init__(self):
        self.__connection = psycopg2.connect("dbname='SkillPlant' host='localhost' user='postgres' password='changeme'")

    def getConnection(self):
        return self.__connection

    def insert_row_into_database(self, data):

        cursor = self.__connection.cursor()
        columns = data.keys()
        values = [data[column] for column in columns]
        values_str_list = ["%s"] * len(values)
        values_str = ", ".join(values_str_list)
        cursor.execute("INSERT INTO song_table ({cols}) VALUES ({vals_str})".format(
            cols=columns, vals_str=values_str), values)

