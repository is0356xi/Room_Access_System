from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import re


class kafka_func():
    def __init__(self, topic_name, prod_flag=True):
        self.topic_name = topic_name
        self.server = '192.168.100.60:9092'

        if prod_flag == True:
            self.producer = KafkaProducer(bootstrap_servers=self.server)
            print(self.producer.bootstrap_connected())
        else:
            self.consumer = KafkaConsumer(topic_name, bootstrap_servers=self.server)


    def send_data(self, data):
        future = self.producer.send(self.topic_name, data.encode()).get(timeout=20)
        print("send: {0}".format(data))

    def send_json(self, dict_data):
        self.producer = KafkaProducer(bootstrap_servers=self.server, value_serializer=lambda m: json.dumps(m).encode('ascii'))

        # dst_ipを正規表現を用いて生成 --> 辞書に追加
        pattern = '.*?:'
        result = re.match(pattern, self.server)
        dst_ip = result.group()[:-1]
        dict_data["dst_ip"] = dst_ip
        print(dict_data)
        future = self.producer.send(self.topic_name, dict_data).get(timeout=20)

        print("send: dict_data")


    def recv_data(self):   
        for msg in self.consumer:
            print("recv: {0}".format(msg.value.decode()))

    def recv_json(self):
        self.consumer = KafkaConsumer(self.topic_name, 
            bootstrap_servers=self.server, 
            value_deserializer=lambda m: json.loads(m.decode('ascii')))

        for msg in self.consumer:
            print(msg)
        


if __name__ == "__main__":
    topic_name = "test"
    kafka_client = kafka_func(topic_name, False)

    # kafka_client.recv_data()