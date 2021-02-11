#!/bin/sh
date=`date '+%Y-%m-%d %H:%M:%S'`

co2=`sudo python3 -m mh_z19 | jq '.co2'`
if [ $? -gt 0 ]; then
	echo "${date},0"
	exit 1;
fi

~/python-venv/RAS/bin/python send_co2.py ${co2} "${date}"