#!/bin/sh
date=`date '+%Y-%m-%d %H:%M:%S'`

odor=`/home/pi/python-venv/RAS/bin/python odor.py`

if [ $? -gt 0 ]; then
	echo "${date},0"
	exit 1;
fi

/home/pi/python-venv/RAS/bin/python send_odor.py ${odor} "${date}"