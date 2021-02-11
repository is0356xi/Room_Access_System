# wlan0がupしていたらdownしておく
sudo ifconfig wlan0 down

# Monitorモードの設定を行う
sudo iwconfig wlan0 mode monitor

# wlan0をupする
sudo ifconfig wlan0 up

# pcapの開始
sudo tcpdump -w ~/pcap/wlan-%F-%T.pcap -G 180 -i wlan0 type data subtype null -s 42 &
