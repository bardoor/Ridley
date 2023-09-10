from flask import Flask, request, jsonify
import queue

app = Flask(__name__)

# Create a thread-safe queue to store incoming data
data_queue = queue.Queue()

@app.route('/store_path', methods=['POST'])
def store_path():
    try:
        # Get the data from the request JSON data
        data = request.get_json()

        # Check if the data is a list of lists
        if isinstance(data, list) and all(isinstance(inner_list, list) for inner_list in data):
            # Put the data into the queue for safe storage
            data_queue.put(data)

            return jsonify({"message": "Path stored safely."}), 200
        else:
            return jsonify({"error": "Invalid input. Expected a list of lists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_path', methods=['GET'])
def get_path():
    try:
        # Get the data from the queue (this will block if the queue is empty)
        data = data_queue.get()

        response = jsonify({'path': data[-1]})
        response.headers.add('Access-Control-Allow-Origin', '*')
        # Return the data as a JSON response
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
