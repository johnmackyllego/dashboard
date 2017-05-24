from ayannahcore.sms.ttypes import Message
from validation import DeserializeThriftMsg
from kafka import KafkaConsumer, TopicPartition
import psycopg2
import datetime
import os

try:
    conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(
        os.getenv('DB_NAME', 'logfile'),
        os.getenv('DB_USER','hmmmacky'),
        os.getenv('DB_HOST','localhost'),
        os.getenv('DB_PASSWORD','hmmmacky'),
    ))
    
    #consumer = KafkaConsumer('incoming-sms', bootstrap_servers='192.168.8.8:9092', auto_offset_reset='earliest')
    consumer = KafkaConsumer('incoming-sms', group_id='smartmoney-acceptance', bootstrap_servers='192.168.8.7:9092')
    
    for msg in consumer:
        sms = DeserializeThriftMsg(Message(), msg.value)
        sms_raw = sms.raw
        sms_sender = sms.sender
        sms_receiver = sms.receiver
        sms_timestamp = datetime.datetime.fromtimestamp(sms.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        query = "SELECT count(raw) FROM consumer_message where raw = '%s'" % (sms_raw)
        
        cur = conn.cursor()
        cur.execute(query)
        a = cur.fetchone()[0]
        conn.commit()
        
        if a < 1:
            print "RAW:       ", sms.raw
            print "SENDER:    ", sms.sender
            print "RECEIVER:  ", sms.receiver
            print "TIMESTAMP: ", sms_timestamp
            print "================================================================================="
            query = "INSERT INTO consumer_message (sender, receiver, raw, timestamp) VALUES (%s, %s, %s, %s);"
            data = (sms_sender, sms_receiver, sms_raw, sms_timestamp)
            cur.execute(query, data)
            conn.commit()
        
        elif a >= 1:
            print "DUPLICATE"
            print "RAW:       ", sms.raw
            print "SENDER:    ", sms.sender
            print "RECEIVER:  ", sms.receiver
            print "TIMESTAMP: ", sms_timestamp
            print "================================================================================="

except:
	print "Unable to connect to database"
    
