#!/usr/bin/env python3
import asyncio
import json
from kafka import KafkaConsumer
import websockets
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
import requests
import uuid

TOPIC = 'cluster-topic1'
GROUP_ID = 'consumer_group_1'
KAFKA_SERVER = 'localhost:9092'
connected_clients = {}  #stores active WebSocket clients and their user data

user_counter = 1
def generate_user_id():
    global user_counter
    user_id = f"u{user_counter:03}"  
    user_counter += 1
    return user_id+'_1'

def poll_kafka_messages(consumer):
    """Poll Kafka messages in a separate thread"""
    messages = consumer.poll(timeout_ms=1000)
    return messages

async def consume_messages():
    """asynchronously consume messages from Kafka and handle broadcasting"""
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
    print("[Sub_1] Kafka consumer started. Listening for messages...")
    
    executor = ThreadPoolExecutor(max_workers=1)
    loop = asyncio.get_event_loop()
    
    while True:
        try:
            raw_messages = await loop.run_in_executor(executor, poll_kafka_messages, consumer)
            for topic_partition, messages in raw_messages.items():
                for message in messages:
                    print(f"[Sub_1] Received Kafka message sub 1: {message.value}")
                    d = message.value
                    d = d.get("emoji")
                    #print("[Sub_1] Sub 1",d)
                    # output = {"emoji":message.value.get("emoji")}
                    await broadcast(message.value)
        except Exception as e:
            print(f"[Sub_1] Error consuming Kafka messages: {e}")
        await asyncio.sleep(0.1)

async def broadcast(message):
    #send a message to all currently connected clients
    if not connected_clients:
        print("[Sub_1] No connected clients to broadcast to")
        return
        
    message_data = message
    # print(message.type())
    # print(message_data.type())
    print(f"[Sub_1] Broadcasting to {len(connected_clients)} clients: {message_data}")
    
    tasks = []
    for websocket, user_data in connected_clients.copy().items():
        try:
            #create async tasks for sending the message to each client
            task = asyncio.create_task(websocket.send(json.dumps(message_data)))
            tasks.append(task)
            print(f"[Sub_1] Sending message to user {user_data['user_id']}")
        except Exception as e:
            print(f"[Sub_1] Error creating send task for user {user_data['user_id']}: {e}")
            
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result, (websocket, user_data) in zip(results, connected_clients.copy().items()):
            if isinstance(result, Exception):
                print(f"[Sub_1] Failed to send to user {user_data['user_id']}: {result}")
                del connected_clients[websocket]

async def send_to_specific_user(user_id, message):
    for websocket, user_data in connected_clients.items():
        if user_data['user_id'] == user_id:
            try:
                await websocket.send(json.dumps(message))
                return True
            except Exception as e:
                print(f"[Sub_1] Error sending to user {user_id}: {e}")
                return False
    return False

async def websocket_handler(websocket):

    # Generate unique user_id
    user_id = str(generate_user_id())
    connected_clients[websocket] = {
        'user_id': user_id,
        'connected_at': asyncio.get_event_loop().time()
    }
    
    print(f"[Sub_1] New client connected. User ID: {user_id}")
    
    try:
        # Send the user_id to the client as acknowledgement
        await websocket.send(json.dumps({
            "type": "connection_ack",
            "user_id": user_id,
            "message": "Connected to server"
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"[Sub_1] Received message from user {user_id}: {data}")
                #print("hello")
                
                #handle specific message types
                if data.get('type') == 'send_to_user':
                    target_user_id = data.get('target_user_id')
                    message_content = data.get('message')
                    if target_user_id and message_content:
                    #attempt to send a direct message to the target user

                        success = await send_to_specific_user(target_user_id, {
                            'type': 'direct_message',
                            'from_user_id': user_id,
                            'message': message_content
                        })
                        await websocket.send(json.dumps({
                            'type': 'send_status',
                            'success': success
                        }))
                
            except json.JSONDecodeError:
                print(f"[Sub_1] Invalid JSON received from user {user_id}")
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[Sub_1] Client {user_id} connection closed normally")
    except Exception as e:
        print(f"[Sub_1] Error with client {user_id}: {e}")
    finally:
        # Notify the API about client disconnection
        subscriber_update_payload = {
            "id": 1
        }
        try:
            response = requests.post("http://localhost:4999/api/unregister", json=subscriber_update_payload)
            if response.status_code == 200:
                print(f"[Sub_1] Updated subscriber registry for client {user_id}")
            else:
                print(f"[Sub_1] Failed to update registry for client {user_id}: {response.json()}")
        except Exception as api_exception:
            print(f"Error sending request to update registry: {api_exception}")

        # Remove the client from the list and log
        del connected_clients[websocket]
        print(f"[Sub_1] Client {user_id} disconnected. Total clients: {len(connected_clients)}")

async def main():
    try:
        ws_server = await websockets.serve(websocket_handler, "localhost", 5001)
        print("[Sub_1] WebSocket server started on ws://localhost:5001")
        kafka_consumer_task = asyncio.create_task(consume_messages())
        await asyncio.gather(
            ws_server.wait_closed(),
            kafka_consumer_task
        )
    except Exception as e:
        print(f"[Sub_1] Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
