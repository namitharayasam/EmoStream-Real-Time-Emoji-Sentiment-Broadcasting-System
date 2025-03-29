from flask import Flask, request, jsonify

app = Flask(__name__)

# Registry of active subscribers with cluster information and capacity
subscribers = [
    {"id": 1, "url": "ws://localhost:5001", "cluster": 1, "clients": [], "capacity": 2},
    {"id": 2, "url": "ws://localhost:5002", "cluster": 1, "clients": [], "capacity": 2},
    {"id": 3, "url": "ws://localhost:5003", "cluster": 2, "clients": [], "capacity": 2},
    {"id": 4, "url": "ws://localhost:5004", "cluster": 2, "clients": [], "capacity": 2}
]

# Maintain round-robin assignment index
round_robin_index = 0


@app.route('/api/register', methods=['POST'])
def register_client():
    data = request.json
    client_name = data.get("client_name")

    if not client_name:
        return jsonify({"error": "Client name is required"}), 400

    # Find the subscriber with the least number of clients
    available_subscriber = None
    min_clients = float('inf')

    for subscriber in subscribers:
        if len(subscriber["clients"]) < subscriber["capacity"] and len(subscriber["clients"]) < min_clients:
            available_subscriber = subscriber
            min_clients = len(subscriber["clients"])

    if available_subscriber:
        # Assign the client to the subscriber
        available_subscriber["clients"].append(client_name)
        return jsonify({
            "message": "Registration successful",
            "subscriber_url": available_subscriber["url"]
        }), 200

    # If no subscriber has capacity
    return jsonify({"error": "All subscribers are full"}), 500

@app.route('/api/unregister', methods = ['POST'])
def unregister():
    data = request.json
    sub_id = data.get("id")

    for sub in subscribers:
        if sub["id"] == sub_id:
            sub["clients"].pop()

    return jsonify({"message": "Client unregistered successfully"}), 200



@app.route('/api/clients', methods=['GET'])
def get_clients():
    # Aggregate all clients from subscribers
    all_clients = [
        {"subscriber_id": sub["id"], "subscriber_url": sub["url"], "clients": sub["clients"]}
        for sub in subscribers
    ]
    return jsonify(all_clients), 200




@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    return jsonify(subscribers), 200


if __name__ == '__main__':
    app.run(port=4999, debug=True)
