from DatabaseKafkaConsumer import DatabaseKafkaConsumer
from Database import Database

import json
import datetime

class DatabaseProxy:

    def __init__(self):
        self.consumer = DatabaseKafkaConsumer().getCustomer()
        self.database = Database().getConnection()

    def delete_duplicates(self):

        cur = self.database.cursor()

        cur.execute("DELETE FROM skillplant_data a USING "
                    "(SELECT MIN(ctid) as ctid, position, region, country, company, seniority FROM skillplant_data GROUP BY position, region, country, company, seniority HAVING COUNT(*) > 1) b "
                    "WHERE a.position = b.position AND a.region = b.region AND a.country = b.country AND a.company = b.company AND a.seniority = b.seniority AND a.ctid <> b.ctid")
        print('Duplicates deleted')
        self.database.commit()

    def insert_row_into_database(self, data):
        cur = self.database.cursor()
        query = """INSERT INTO skillplant_data 
                   (position, company, date_updated, region, country, description, remote, job_type, seniority, date_gathered,hard_skill_1,hard_skill_2,hard_skill_3,hard_skill_4,hard_skill_5,soft_skill_1,soft_skill_2,soft_skill_3,soft_skill_4,soft_skill_5) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s)"""

        date_updated = datetime.datetime.strptime(data['updated'], "%d/%m/%Y").date()
        date_gathered = datetime.datetime.strptime(data['date_gathered'], "%d/%m/%Y %H:%M:%S").date()
        val = (data['title'], data['company'], date_updated, data['region'], data['country'], data['description'], data['remote_type'], data['employment_type'], data['seniority'], date_gathered, data["Hard Skill"][0],data["Hard Skill"][1],data["Hard Skill"][2], data["Hard Skill"][3], data["Hard Skill"][4],data["Soft Skill"][0],data["Soft Skill"][1],data["Soft Skill"][2], data["Soft Skill"][3], data["Soft Skill"][4])

        cur.execute(query, val)
        self.database.commit()

    def consume_broker_messages(self):

        self.consumer.subscribe(['user-tracker'])
        print(self.database)
        while True:
            message = self.consumer.poll(60.0)  # timeout
            if message is None:
                self.delete_duplicates()
                continue
            if message.error():
                print('Error: {}'.format(message.error()))
                continue

            data = message.value().decode('utf-8')
            self.insert_row_into_database(json.loads(data, strict=False))

        self.consumer.close()


if __name__ == '__main__':
    dbProxy = DatabaseProxy()
    dbProxy.consume_broker_messages()
