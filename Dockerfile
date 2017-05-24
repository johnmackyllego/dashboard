FROM python:2.7

ENV PYTHONUNBUFFERED 1

#NOTE:

#if you use company proxy please configure the ENV

#else if you use your own connection just remove the ENV

ENV http_proxy 'http://192.168.8.7:3128'

ENV HTTP_PROXY 'http://192.168.8.7:3128'

ENV https_proxy 'http://192.168.8.7:3128'

ENV HTTPS_PROXY 'http://192.168.8.7:3128'

#RUN mkdir /kafka

#WORKDIR /kafka

#COPY requirements.txt /kafka/

#COPY . /kafka

#RUN pip --default-timeout=60 install -r requirements.txt

#EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN apt-get -y update && apt-get -y upgrade \

    && mkdir /var/log/supervisor

COPY . /opt/

WORKDIR /opt/

RUN mv etc/* /etc/

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/opt/entrypoint.sh"]

