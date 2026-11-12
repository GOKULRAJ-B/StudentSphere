FROM manios/nagios:latest

USER root

RUN apk add --no-cache py3-pip

RUN python3 -m pip install --break-system-packages pymongo

COPY etc/ /opt/nagios/etc/
COPY check_mongodb.py /opt/nagios/libexec/check_mongodb.py

RUN chmod 755 /opt/nagios/libexec/check_mongodb.py \
    && chown -R nagios:nagios /opt/nagios/etc \
    && chown nagios:nagios /opt/nagios/libexec/check_mongodb.py