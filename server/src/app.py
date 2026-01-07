from flask import Flask, request, jsonify
from flask_cors import CORS
from src.ocr import OCRNeuralNetwork
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with empty training data
# In a real application, you would load actual training data
data_matrix = np.zeros((100, 400))  # Placeholder: 100 samples, 400 features (20x20 pixels)
data_labels = list(range(10)) * 10  # Placeholder labels
training_indices = list(range(100))

# Initialize the neural network
nn = OCRNeuralNetwork(20, data_matrix, data_labels, training_indices, use_file=True)


@app.route('/', methods=['POST'])
def handle_request():
    """Handle training and prediction requests"""
    try:
        try:
            payload = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400
   
        if not payload:
            return jsonify({"error": "Invalid JSON"}), 400

        if payload.get('train'):
            train_array = payload.get('trainArray')
            if not train_array:
                return jsonify({"error": "trainArray is required"}), 400

            nn.train(train_array)
            nn.save()
            return jsonify({"success": True, "message": "Training completed"}), 200

        elif payload.get('predict'):
            image = payload.get('image')
            if image is None:
                return jsonify({"error": "image is required"}), 400

            try:
                result = nn.predict(image)
                return jsonify({
                    "type": "test",
                    "result": result
                }), 200
            except Exception as e:
                return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

        else:
            return jsonify({"error": "Invalid request. Use 'train' or 'predict'"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "OCR server is running"}), 200


def create_app():
    """Application factory for testing"""
    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f'Starting OCR Flask server on port {port}...')
    app.run(host='0.0.0.0', port=port, debug=False)
