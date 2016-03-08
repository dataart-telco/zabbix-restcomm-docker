#!/bin/bash

echo "*************"
echo "Start restcomm import content script"

ZABBIX_SERVER=http://localhost

until $(curl --output /dev/null --silent --head --fail $ZABBIX_SERVER); do
    printf '...wait for zabbix server'
    sleep 5
done

WORK_DIR=/opt/zabbix_content
$WORK_DIR/import_all.py $WORK_DIR/restcomm $ZABBIX_SERVER

echo "*************"
echo "End restcomm import content script"