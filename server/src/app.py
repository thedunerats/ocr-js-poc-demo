from flask import Flask, request, jsonify
from flask_cors import CORS
from src.ocr import OCRNeuralNetwork
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize with empty training data
# In a real application, you would load actual training data
data_matrix = np.zeros(
    (100, 400)
)  # Placeholder: 100 samples, 400 features (20x20 pixels)
data_labels = list(range(10)) * 10  # Placeholder labels
training_indices = list(range(100))

# Initialize the neural network
nn = OCRNeuralNetwork(20, data_matrix, data_labels, training_indices, use_file=True)


@app.route("/", methods=["POST"])
def handle_request():
    """Handle training and prediction requests"""
    try:
        try:
            payload = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400

        if not payload:
            return jsonify({"error": "Invalid JSON"}), 400

        if payload.get("train"):
            train_array = payload.get("trainArray")
            if not train_array:
                return jsonify({"error": "trainArray is required"}), 400

            # Validate training data
            try:
                for i, data in enumerate(train_array):
                    if "y0" not in data or "label" not in data:
                        return (
                            jsonify(
                                {"error": f"Sample {i}: Missing 'y0' or 'label' field"}
                            ),
                            400,
                        )

                    if len(data["y0"]) != 400:
                        return (
                            jsonify(
                                {
                                    "error": f"Sample {i}: Expected 400 pixels, got {len(data['y0'])}"
                                }
                            ),
                            400,
                        )

                    label = data["label"]
                    if not isinstance(label, int) or label < 0 or label > 9:
                        return (
                            jsonify(
                                {
                                    "error": f"Sample {i}: Label must be an integer between 0-9, got {label}"
                                }
                            ),
                            400,
                        )

                    # Validate that all pixel values are numeric
                    try:
                        for pixel_idx, pixel_val in enumerate(data["y0"]):
                            float(pixel_val)
                    except (ValueError, TypeError) as e:
                        return (
                            jsonify(
                                {
                                    "error": f"Sample {i}, pixel {pixel_idx}: Invalid value '{pixel_val}' - {str(e)}"
                                }
                            ),
                            400,
                        )

            except Exception as e:
                return (
                    jsonify({"error": f"Invalid training data format: {str(e)}"}),
                    400,
                )

            try:
                print(f"[DEBUG] Starting training with {len(train_array)} samples")
                for idx, sample in enumerate(train_array):
                    print(
                        f"[DEBUG] Sample {idx}: label={sample.get('label')}, y0_length={len(sample.get('y0', []))}, y0_sample={sample.get('y0', [])[:5]}..."
                    )
                nn.train(train_array)
                print(f"[DEBUG] Training completed successfully")
                nn.save()
                print(f"[DEBUG] Model saved successfully")
                return jsonify({"success": True, "message": "Training completed"}), 200
            except Exception as e:
                import traceback

                error_details = traceback.format_exc()
                print(f"[ERROR] Training failed: {error_details}")
                return jsonify({"error": f"Training failed: {str(e)}"}), 500

        elif payload.get("predict"):
            image = payload.get("image")
            if image is None:
                return jsonify({"error": "image is required"}), 400

            # Validate image data
            if not isinstance(image, list):
                return jsonify({"error": "image must be an array"}), 400

            if len(image) != 400:
                return (
                    jsonify(
                        {"error": f"image must contain 400 pixels, got {len(image)}"}
                    ),
                    400,
                )

            try:
                # Ensure all values are numeric
                image = [float(x) for x in image]
            except (ValueError, TypeError) as e:
                return (
                    jsonify({"error": f"image must contain numeric values: {str(e)}"}),
                    400,
                )

            try:
                result = nn.predict(image)
                return jsonify({"type": "test", "result": result}), 200
            except Exception as e:
                return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

        else:
            return jsonify({"error": "Invalid request. Use 'train' or 'predict'"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "OCR server is running"}), 200


def create_app():
    """Application factory for testing"""
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"Starting OCR Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
