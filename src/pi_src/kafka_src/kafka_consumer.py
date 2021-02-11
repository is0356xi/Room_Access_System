import kafka_func
import time

kafka = kafka_func.kafka_func("test", False)

kafka.recv_json()