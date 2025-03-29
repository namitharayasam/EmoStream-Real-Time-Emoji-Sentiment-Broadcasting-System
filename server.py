from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

producer = KafkaProducer(value_serializer=lambda x: json.dumps(x).encode('utf-8'))

@app.route('/emoji', methods=['POST'])
def handle_emoji_data():

    data = request.get_json()
    # user_id = data['user_id']
    # emoji_type = data['emoji_type']
    # timestamp = data['timestamp']

    producer.send('emoji', value=data)
    producer.flush()
    return 'Emoji data received', 200

    # return jsonify({'message': 'Emoji data received and queued'}), 200

if __name__ == '__main__':
    app.run(debug=True)
