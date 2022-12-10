from confluent_kafka import Consumer


class DatabaseProxy:

    def consume_broker_messages(self):
        consumer = Consumer(
            {'bootstrap.servers': 'localhost:9092', 'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})

        consumer.subscribe(['user-tracker'])

        while True:
            message = consumer.poll(1.0)  # timeout
            if message is None:
                continue
            if message.error():
                print('Error: {}'.format(message.error()))
                continue
            data = message.value().decode('utf-8')
            print(data)
        consumer.close()


if __name__ == '__main__':
    dbProxy = DatabaseProxy()
    dbProxy.consume_broker_messages()