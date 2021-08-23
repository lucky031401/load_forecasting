#!/bin/sh
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
source /root/.bash_profile

now="$(date +'%Y_%m_%d')"
prev="$(date -d 'yesterday' +%Y_%m_%d)"
/usr/bin/curl -o /home/g22qkqkq/load-forecast/data/loadfueltype/$prev.csv https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadfueltype_1.csv
#cd ../loadfuelareas
/usr/bin/curl -o /home/g22qkqkq/load-forecast/data/loadfuelareas/$now.csv https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv
~    
