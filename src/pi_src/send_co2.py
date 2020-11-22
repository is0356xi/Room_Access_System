import kafka_func
import sys
from datetime import datetime as dt

args = sys.argv

def main():
    topic_name = "co2"
    kafka = kafka_func.kafka_func(topic_name, True)

    data = dict(co2=int(args[1]), time=args[2])
    kafka.send_json(data)

if __name__ == "__main__":
    main()
    