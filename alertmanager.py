from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Define the memory consumption threshold (in percentage)
MEMORY_THRESHOLD_PERCENT = 80  # Example threshold

@app.route('/alert', methods=['POST'])
def handle_alert():
    # Parse the incoming JSON data
    data = request.json
    print("Received data:", json.dumps(data, indent=4))  # Print the received JSON for debugging

    # Example of how the data might be structured. This will need to be adjusted
    # based on the actual structure of the Alertmanager webhook payload
    for alert in data.get('alerts', []):
        labels = alert.get('labels', {})
        annotations = alert.get('annotations', {})
        
        # Extract pod IP, current memory usage, and total memory capacity
        pod_ip = labels.get('instance')
        current_memory_usage = float(annotations.get('currentMemoryUsage', '0').replace('MB', ''))
        total_memory_capacity = float(annotations.get('totalMemoryCapacity', '0').replace('MB', ''))

        # Compute memory consumption percentage
        if total_memory_capacity > 0:  # Prevent division by zero
            memory_consumption_percent = (current_memory_usage / total_memory_capacity) * 100

            # Check if memory consumption percentage is over the threshold
            if memory_consumption_percent > MEMORY_THRESHOLD_PERCENT:
                # Perform the specified action here
                print(f"Memory consumption over threshold for pod {pod_ip}: {memory_consumption_percent:.2f}%")
                # Example action: log, send notification, etc.

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)