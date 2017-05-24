from kafka import KafkaConsumer
from ayannahcore.sms.ttypes import Message
from validation import DeserializeThriftMsg
import psycopg2
import datetime

try:
    conn = psycopg2.connect("dbname='logfile' user='hmmmacky' host='localhost' password='hmmmacky'")
except:
    print "I am unable to connect to the database"
    
consumer = KafkaConsumer(
        'incoming-sms',
        bootstrap_servers = '192.168.8.8:9092',
        auto_offset_reset='earliest',
        group_id=None
    )        

cursor = conn.cursor()

for msg in consumer:
    sms = DeserializeThriftMsg(Message(), msg.value)
    sms_raw = sms.raw

    fetch = cursor.execute('select count(raw) from consumer_message where raw = %;', (sms_raw,))
    print "==========================================================================================="
    print fetch
    print "-------------------------------------------------------------------------------------------"
    print sms_raw
    
