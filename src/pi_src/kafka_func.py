from kafka import KafkaProducer
from kafka import KafkaConsumer
import json


class kafka_func():
    def __init__(self, topic_name, prod_flag):
        self.topic_name = topic_name

        if prod_flag == True:
            self.producer = KafkaProducer(bootstrap_servers='192.168.100.68:9092')
            print(self.producer.bootstrap_connected())
        else:
            self.consumer = KafkaConsumer(topic_name, bootstrap_servers='192.168.100.68:9092')


    def send_data(self, data):
        future = self.producer.send(self.topic_name, data.encode()).get(timeout=10)
        print("send: {0}".format(data))

    def send_json(self, dict_data):
        self.producer = KafkaProducer(bootstrap_servers='192.168.100.68:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))
        future = self.producer.send(self.topic_name, dict_data).get(timeout=10)

        print("send: dict_data")


    def recv_data(self):   
        for msg in self.consumer:
            print("recv: {0}".format(msg.value.decode()))

    def recv_json(self):
        self.consumer = KafkaConsumer(self.topic_name, 
            bootstrap_servers='192.168.100.68:9092', 
            value_deserializer=lambda m: json.loads(m.decode('ascii')))

        for msg in self.consumer:
            print(msg)
        


if __name__ == "__main__":
    topic_name = "test"
    kafka_client = kafka_func(topic_name, False)

    # kafka_client.recv_data()