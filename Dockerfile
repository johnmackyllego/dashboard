FROM python:2.7

MAINTAINER Zorex Salvo, PUP-CS May 2017 Interns

RUN apt-get -y update \
    && mkdir /var/log/supervisor

COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

COPY . /opt/
WORKDIR /opt/
RUN mv etc/* /etc/

EXPOSE 8000

ENTRYPOINT ["/opt/entrypoint.sh"]
