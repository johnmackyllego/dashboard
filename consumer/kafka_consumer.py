from ayannahcore.sms.ttypes import Message
from validation import DeserializeThriftMsg
from kafka import KafkaConsumer, TopicPartition
import psycopg2
import datetime
import os

TOPIC = os.getenv('KAFKA_TOPIC', 'incoming-sms')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'smartmoney-acceptance')
KAFKA_HOST = os.getenv('KAFKA_HOST', '192.168.8.7')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')

conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(
			os.getenv('DB_NAME', 'smsdb'),
			os.getenv('DB_USER','postgres'),
			os.getenv('DB_HOST','sms-db'),
			os.getenv('DB_PASSWORD','postgres'),
			))

consumer = KafkaConsumer(TOPIC,
		     group_id=KAFKA_GROUP_ID,
		     bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT),
		     auto_offset_reset='earliest',
		     enable_auto_commit=False)

for msg in consumer:
    sms = DeserializeThriftMsg(Message(), msg.value)
    sms_raw = sms.raw
    sms_sender = sms.sender
    sms_receiver = sms.receiver
    sms_timestamp = datetime.datetime.fromtimestamp(sms.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    print('================')
    print(sms)

    try:
    	query = "SELECT count(raw) FROM consumer_message where raw = '{}'".format(sms_raw)
	cur = conn.cursor()
	cur.execute(query)
	a = cur.fetchone()[0]
	conn.commit()
    except Exception as e:
	print(e)

    if a < 1:
	try:
	    query = '''INSERT INTO consumer_message (sender, receiver, raw, timestamp) VALUES (%s, %s, %s, %s);'''
	    data = (sms_sender, sms_receiver, sms_raw, sms_timestamp)
	    cur.execute(query, data)
            conn.commit()
	    print('RAW: {}'.format(sms.raw))
	except Exception as e:
	    print(e)
            print('Malformed sms: {}'.format(sms.raw))

    elif a >= 1:
	print('DUPLICATE: {}'.format(sms_raw))
