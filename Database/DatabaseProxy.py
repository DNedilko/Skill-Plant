from DatabaseKafkaConsumer import DatabaseKafkaConsumer
from Database import Database
import json
# from description_parser import skills_extractor

class DatabaseProxy:

    def __init__(self):
        self.consumer = DatabaseKafkaConsumer().getCustomer()
        self.database = Database()

    def is_duplicte(self, data):
        cur = self.Database.cursor()

        # Select all rows from the table where all columns are the same as the current row
        cur.execute(
            "SELECT * FROM mytable t1 WHERE EXISTS (SELECT * FROM mytable t2 WHERE t1.col1 = t2.col1 AND t1.col2 = t2.col2 AND t1.col3 = t2.col3 AND t1.col4 = t2.col4 AND t1.col5 = t2.col5)")

        # Fetch the rows
        rows = cur.fetchall()

        if len(rows) > 0:
            return False
        else:
            return True


    def insert_row_into_database(self, data):
        pass

    def consume_broker_messages(self):

        self.consumer.subscribe(['user-tracker'])

        while True:
            message = self.consumer.poll(1.0)  # timeout
            if message is None:
                continue
            if message.error():
                print('Error: {}'.format(message.error()))
                continue
            data = json.loads(message.value().decode('utf-8'))
            self.database.insert_row_into_database(data)
            print(data.keys())
        self.consumer.close()


if __name__ == '__main__':
    dbProxy = DatabaseProxy()
    dbProxy.consume_broker_messages()