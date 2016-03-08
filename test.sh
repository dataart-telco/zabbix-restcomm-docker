docker rm -f zabbix

docker run \
    -d \
    --name zabbix \
    -p 80:80 \
    -p 10051:10051 \
    -v /etc/localtime:/etc/localtime:ro \
    --env="ZS_DBHost=192.168.122.2" \
    --env="ZS_DBPort=31306" \
    --env="ZS_DBUser=zabbix" \
    --env="ZS_DBPassword=my_password" \
    zabbix-restcomm

docker exec -it zabbix bash

