import asyncio
import websockets
import json
import requests
import time
import random
import threading

class WebSocketClient:
    def __init__(self):
        self.user_id = None
        self.websocket = None

    async def listen(self, uri):
        """
        Connect to the WebSocket server and listen for incoming messages.
        This function continuously receives and processes messages from the server.
        """
        try:
            print(f"[Client 1] Trying to connect to {uri}")
            
            # Establish connection to the WebSocket server
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                print("[Client 1] Connected to WebSocket server.")
                
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)

                        # This is executed the first time the client receives and sets its dynamically generated user_id
                        if data.get('type') == 'connection_ack':
                            self.user_id = data.get('user_id')
                            print(f"[Client 1] Received user_id: {self.user_id}")
                            
                            send_emojis = input("Do you want to send emojis? (yes/no): ").strip().lower()
                            if send_emojis == 'yes':
                                start_emoji_threads(self.user_id)

                        # The client constantly prints the broadcasted data it receives from the subscribers
                        print(f"[Client 1] Received message: {data.get('emoji')}")

                    except websockets.exceptions.ConnectionClosed as e:
                        print("[Client 1] Connection closed:", e)
                        break

        except Exception as e:
            print(f"[Client 1] Error during WebSocket connection: {e}")
        finally:
            self.websocket = None
            print("[Client 1] Disconnected from WebSocket server.")

def send_emoji(user_id):
    # Sends random emoji to the server as a POST request
    while True:
        emoji = ['\U0001f4af', '\U0001f525', '\U0001f44f', '\u2764\ufe0f', '\U0001f60a']
        emoji_type = random.choice(emoji)
        timestamp = time.time()
        data = {
            'user_id': user_id,
            'emoji_type': emoji_type,
            'timestamp': timestamp
        }

        try:
            response = requests.post('http://localhost:5000/emoji', json=data)
        except requests.exceptions.RequestException as e:
            print(f"[Client 1] Request failed for {user_id}: {e}")
        
        # Sleep briefly to avoid overwhelming the server
        time.sleep(0.005)

def start_emoji_threads(user_id):
    """
    Starts multiple threads to send emojis concurrently for the given user_id.
    Creates 3 threads, each running the send_emoji function.
    """
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=send_emoji, args=(user_id,))
        thread.start()
        threads.append(thread)

    print(f"[Client 1] Started 3 emoji threads for user {user_id}.")

async def main():
    client = WebSocketClient()

    # API endpoint
    url = "http://localhost:4999/api/register"

    # Data to send
    payload = {"client_name": "ClientA"}

    # Send POST request
    response = requests.post(url, json=payload)

    # Access the JSON response
    if response.status_code == 200:
        data = response.json()
        subscriber_url = data.get("subscriber_url")
        print(f"[Client 1] Registration successful! Assigned subscriber: {subscriber_url}")
    else:
        print(f"[Client 1] Error: {response.text}")

    listener_task = asyncio.create_task(client.listen(subscriber_url))

    # Wait until the user ID is assigned by the server
    while not client.user_id:
        await asyncio.sleep(0.1)

    await listener_task

if __name__ == "__main__":
    asyncio.run(main())

