#!/bin/sh
date=`date '+%Y-%m-%d %H:%M:%S'`

sensor_vals=`/home/pi/python-venv/RAS/bin/python get_sensor_val.py`



if [ $? -gt 0 ]; then
	echo "${date},0"
	exit 1;
fi

/home/pi/python-venv/RAS/bin/python send_sensor_val.py "${sensor_vals}" "${date}"