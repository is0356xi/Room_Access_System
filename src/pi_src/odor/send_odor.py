
import sys
sys.path.append('../')

from kafka_src import kafka_func
import sys
from datetime import datetime as dt

# ipアドレスを取得する
import re
import ipget

args = sys.argv

def get_ip():
    # ipアドレスを取得
    a = ipget.ipget()
    ip_cidr = a.ipaddr("wlan0")


    # CIDR表記を直す
    content = r'{0}'.format(ip_cidr)
    pattern = '([0-9]{1,3}.){3}[0-9]{1,3}'
    repatter = re.compile(pattern)
    result = repatter.match(content)

    ip = result.group()
    
    return ip

def main():
    topic_name = "odor-rpi3"
    kafka = kafka_func.kafka_func(topic_name, True)

    data = dict(odor=float(args[1]), time=args[2], device_id="Rpi3", src_ip=get_ip())
    print(data)
    kafka.send_json(data)

if __name__ == "__main__":
    main()
    # pass
    
