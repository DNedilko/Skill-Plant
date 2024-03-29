from DatabaseKafkaConsumer import DatabaseKafkaConsumer
from Database import Database

import json
import datetime

class DatabaseProxy:

    def __init__(self):
        self.consumer = DatabaseKafkaConsumer().getCustomer()
        self.database = Database().getConnection()

    def is_duplicate(self, data):
        cur = self.database.cursor()

        # Select all rows from the table where all columns are the same as the current row
        cur.execute(
            """SELECT * FROM skillplant_data t1 WHERE t1.position = '{position}' AND t1.company = '{company}' AND t1.region = '{region}' AND t1.country = '{country}' AND t1.seniority = '{seniority}'""".format
            (position=data['title'].replace("'","''"), company=data['company'].replace("'","''"), region=data['region'].replace("'","''"), country=data['country'].replace("'","''"), seniority=data['seniority']))

        # Fetch the rows
        rows = cur.fetchall()

        return len(rows) > 0


    def insert_row_into_database(self, data):
        cur = self.database.cursor()
        query = """INSERT INTO skillplant_data 
                   (position, company, date_updated, region, country, description, remote, job_type, seniority, date_gathered,hard_skill_1,hard_skill_2,hard_skill_3,hard_skill_4,hard_skill_5,soft_skill_1,soft_skill_2,soft_skill_3,soft_skill_4,soft_skill_5) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s)"""

        date_updated = datetime.datetime.strptime(data['updated'], "%d/%m/%Y").date()
        date_gathered = datetime.datetime.strptime(data['date_gathered'], "%d/%m/%Y %H:%M:%S").date()
        val = (data['title'].replace("'","''"), data['company'].replace("'","''"), date_updated, data['region'].replace("'","''"), data['country'].replace("'","''"), data['description'].replace("'","''"), data['remote_type'], data['employment_type'], data['seniority'], date_gathered, data["Hard Skill"][0],data["Hard Skill"][1],data["Hard Skill"][2], data["Hard Skill"][3], data["Hard Skill"][4],data["Soft Skill"][0],data["Soft Skill"][1],data["Soft Skill"][2], data["Soft Skill"][3], data["Soft Skill"][4])

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

            data = message.value().decode('utf-8')
            data = json.loads(data, strict=False)

            try:
                if not self.is_duplicate(data):
                    self.insert_row_into_database(data)
            except Exception as i:
                print(f"Error {i}")
                continue

        self.consumer.close()


if __name__ == '__main__':
    dbProxy = DatabaseProxy()
    dbProxy.consume_broker_messages()
