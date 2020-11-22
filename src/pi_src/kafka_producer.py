import kafka_func
import time

kafka = kafka_func.kafka_func("test", True)

while True:
    msg = "aaaa"
    kafka.send_data(msg)
    time.sleep(3)
