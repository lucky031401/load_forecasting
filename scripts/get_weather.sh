 
#!/bin/sh
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
source /root/.bash_profile
now="$(date +'%Y_%m_%d')"
prev="$(date -d 'yesterday' +%Y_%m_%d)"

for i in $(seq 1 4 92);
do
if [[ $i -gt 10 ]]
then
        echo "get F-D0047-0$i"
        /usr/bin/curl -o /home/g22qkqkq/load-forecast/data/weather/F-D0047-0$i/F-D0047-0$i-$now.json -X GET "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-0$i?Authorization=CWB-346A3ABE-DFEB-4F72-945E-53501CD3B8CE" -H  "accept: application/json"
        else
        echo "get F-D0047-00$i"  
        /usr/bin/curl -o /home/g22qkqkq/load-forecast/data/weather/F-D0047-00$i/F-D0047-00$i-$now.json -X GET "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-00$i?Authorization=CWB-346A3ABE-DFEB-4F72-945E-53501CD3B8CE" -H  "accept: application/json"
fi
done

