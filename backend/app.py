from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}})  # Allows all origins for all routes

@app.route('/detect', methods=['POST'])
def detect_entry_type():
    try:
        data = request.json
        typing_data = data.get('typingData', [])
        paste_detected = data.get('pasteDetected', False)

        # Debugging: Log received data
        print("Received Data:", data)

        if paste_detected:
            return jsonify({'entryType': 'copy-pasted'})

        intervals = [typing_data[i]['time'] - typing_data[i - 1]['time'] for i in range(1, len(typing_data))]
        if not intervals:
            return jsonify({'entryType': 'typed'})

        avg_interval = sum(intervals) / len(intervals)
        likely_typed = avg_interval > 100  # Adjust threshold if needed

        return jsonify({'entryType': 'typed' if likely_typed else 'copy-pasted'})
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
