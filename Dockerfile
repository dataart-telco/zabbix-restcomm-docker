FROM zabbix/zabbix-3.0
MAINTAINER Gennadiy Dubina <gdubina@dataart.com>

RUN yum install -y python-pip && \
  pip install --upgrade pip && \
  pip install pyzabbix && \
  yum autoremove -y python-pip

ENV WORK_DIR /opt/restcomm/
RUN mkdir -p $WORK_DIR

ADD conf/jujuapi.yaml $WORK_DIR/jujuapi.yaml
ADD conf/jujuapicli $WORK_DIR/jujuapicli
ADD conf/zabbixapi.yaml $WORK_DIR/zabbixapi.yaml
ADD conf/delete_host.py $WORK_DIR/delete_host.py
ADD conf/restcomm_scale $WORK_DIR/restcomm_scale

ADD files/zabbix_content /opt/zabbix_content
ADD files/import_content.sh /opt/zabbix_content/restcomm_import.sh
ADD files/import_contentd.sh /config/init/restcomm_importd.sh
