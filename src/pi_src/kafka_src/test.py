import re

server = "192.168.100.60:9092"
pattern = '.*?:'

result = re.match(pattern, server)

print(result.group()[:-1])
