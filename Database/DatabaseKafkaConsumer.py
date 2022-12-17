from confluent_kafka import Consumer


class DatabaseKafkaConsumer:

    def __init__(self):
        self.__consumer = Consumer(
            {'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})

    def getCustomer(self):
        return self.__consumer
