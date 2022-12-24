from DatabaseKafkaConsumer import DatabaseKafkaConsumer
from Database import Database
import json
# from description_parser import skills_extractor

class DatabaseProxy:

    def __init__(self):
        self.consumer = DatabaseKafkaConsumer().getCustomer()
        self.database = Database()

    def is_duplicte(self, data):
        pass

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