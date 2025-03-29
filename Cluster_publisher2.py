from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka consumer for receiving data from main publisher
main_consumer = KafkaConsumer('cluster-topic', 
                              bootstrap_servers='localhost:9092',
                              value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Kafka producer for cluster-specific topic
cluster_publisher = KafkaProducer(bootstrap_servers='localhost:9092', 
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("[ClusterPub_2] Starting Cluster Publisher 2...")
for message in main_consumer:
    data = message.value
    # Process and forward to cluster-specific topic
    cluster_publisher.send('cluster-topic2', value=data)
