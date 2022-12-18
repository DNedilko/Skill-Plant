from DatabaseKafkaConsumer import DatabaseKafkaConsumer
from Database import Database

import json
import datetime

class DatabaseProxy:

    def __init__(self):
        self.consumer = DatabaseKafkaConsumer().getCustomer()
        self.database = Database().getConnection()

    def is_duplicte(self, data):
        pass

    def insert_row_into_database(self, data):
        cur = self.database.cursor()
        query = """INSERT INTO skillplant_data 
                   (position, company, date_updated, region, country, description, remote, job_type, seniority, date_gathered) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        date_updated = datetime.datetime.strptime(data['updated'], "%d/%m/%Y").date()
        date_gathered = datetime.datetime.strptime(data['date_gathered'], "%d/%m/%Y %H:%M:%S").date()
        val = (data['title'], data['company'], date_updated, data['region'], data['country'], data['description'], data['remote_type'], data['employment_type'], data['seniority'], date_gathered)

        cur.execute(query, val)
        self.database.commit()

    def consume_broker_messages(self):

        self.consumer.subscribe(['user-tracker'])
        print(self.database)
        while True:
            message = self.consumer.poll(1.0)  # timeout
            if message is None:
                continue
            if message.error():
                print('Error: {}'.format(message.error()))
                continue

            # data = message.value().decode('utf-8')
            data = message.value()

            self.insert_row_into_database(json.loads(data, strict=False))

        self.consumer.close()


if __name__ == '__main__':
    dbProxy = DatabaseProxy()
    dbProxy.consume_broker_messages()