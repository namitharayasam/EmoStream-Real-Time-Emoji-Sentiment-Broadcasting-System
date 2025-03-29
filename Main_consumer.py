from kafka import KafkaConsumer, KafkaProducer
import json
from sparkjob import get_emoji #custom function for emoji data processing
import time

consumer = KafkaConsumer('emoji',value_deserializer=lambda x: json.loads(x.decode('utf-8')))
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  #convert dict to JSON and encode
)

buff = []  #buffer to store emojis for processing
count = 0  #counter for tracking number of emojis processed
last_execution = time.time()

for emoji in consumer:
	count+=1
	buff_time = time.time()-last_execution
	
	#process batch if buffer reaches 1000 emojis or 2 seconds have 
	if count>=1000 or (buff_time>=2 and count!=0):
		#buff.append(emoji.value)
		print("Emojis per second:",count/buff_time)
		
		start_time = time.time() #measure Spark processing time
		most_used_emojis = get_emoji(buff)
		print("Time to process Emoji Data in Spark:",time.time()-start_time)
		
		count = 0 #reset counter
		buff = [] #clear buffer
		
		last_execution = time.time()
		
		print(most_used_emojis)
		for most_used_emoji in most_used_emojis:
			output = {"emoji":most_used_emoji}
			producer.send('emoji-aggregated-data',output) 
	else:
		buff.append(emoji.value)
