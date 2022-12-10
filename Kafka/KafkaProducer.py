import logging
import time
import json

from confluent_kafka import Producer


class KafkaProducer:

    def set_logger(self):

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='producer.log',
                            filemode='w')

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

    def receipt(self, error, message):

        logger = self.set_logger()
        if error is not None:
            print('Error: {}'.format(error))
        else:
            message_result = 'Produced message on topic {} with value of {}\n'.format(message.topic(),
                                                                                      message.value().decode('utf-8'))
            logger.info(message_result)
            print(message_result)

    def produce_broker_message(self, data):

        producer = Producer({'bootstrap.servers': 'localhost:9092'})
        data_json = json.dumps(data)
        producer.poll(1)
        producer.produce('user-tracker', data_json.encode('utf-8'), callback=self.receipt)
        producer.flush()
        time.sleep(3)