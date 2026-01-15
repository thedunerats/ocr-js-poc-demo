from flask import Flask, request, jsonify
from flask_cors import CORS
from src.ocr import OCRNeuralNetwork
from src.neural_network_design import find_optimal_hidden_nodes
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
                        error_msg = (
                            f"Sample {i}, pixel {pixel_idx}: "
                            f"Invalid value '{pixel_val}' - {str(e)}"
                        )
                        return (
                            jsonify({"error": error_msg}),
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
                    label = sample.get("label")
                    y0_length = len(sample.get("y0", []))
                    y0_sample = sample.get("y0", [])[:5]
                    print(
                        f"[DEBUG] Sample {idx}: label={label}, "
                        f"y0_length={y0_length}, y0_sample={y0_sample}..."
                    )
                nn.train(train_array)
                print("[DEBUG] Training completed successfully")
                nn.save()
                print("[DEBUG] Model saved successfully")
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


@app.route("/optimize", methods=["POST"])
def optimize_network():
    """
    Find optimal number of hidden nodes for the neural network
    
    This endpoint trains multiple neural networks with different hidden node counts
    and returns the configuration that performs best on the provided test data.
    
    Request body:
    {
        "trainingData": [{"y0": [...400 values...], "label": 0-9}, ...],
        "testData": [{"y0": [...400 values...], "label": 0-9}, ...],
        "minNodes": 5 (optional, default: 5),
        "maxNodes": 50 (optional, default: 50),
        "step": 5 (optional, default: 5)
    }
    
    Response:
    {
        "results": [
            {"hiddenNodes": 20, "accuracy": 0.95},
            {"hiddenNodes": 25, "accuracy": 0.94},
            ...
        ],
        "optimal": {"hiddenNodes": 20, "accuracy": 0.95},
        "message": "Optimization completed. Tested 9 configurations."
    }
    """
    try:
        try:
            payload = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400

        if not payload:
            return jsonify({"error": "Invalid JSON"}), 400

        # Validate required fields
        training_data = payload.get("trainingData")
        test_data = payload.get("testData")

        if training_data is None or test_data is None:
            return jsonify({
                "error": "Both 'trainingData' and 'testData' are required"
            }), 400

        if not isinstance(training_data, list) or not isinstance(test_data, list):
            return jsonify({
                "error": "trainingData and testData must be arrays"
            }), 400

        if len(training_data) == 0:
            return jsonify({
                "error": "trainingData cannot be empty"
            }), 400

        if len(test_data) == 0:
            return jsonify({
                "error": "testData cannot be empty"
            }), 400

        # Optional parameters
        min_nodes = payload.get("minNodes", 5)
        max_nodes = payload.get("maxNodes", 50)
        step = payload.get("step", 5)

        # Validate parameters
        if not isinstance(min_nodes, int) or min_nodes < 1:
            return jsonify({"error": "minNodes must be a positive integer"}), 400
        if not isinstance(max_nodes, int) or max_nodes <= min_nodes:
            return jsonify({"error": "maxNodes must be greater than minNodes"}), 400
        if not isinstance(step, int) or step < 1:
            return jsonify({"error": "step must be a positive integer"}), 400

        # Validate data format
        all_data = training_data + test_data
        for i, sample in enumerate(all_data):
            if "y0" not in sample or "label" not in sample:
                return jsonify({
                    "error": f"Sample {i}: Missing 'y0' or 'label' field"
                }), 400

            if len(sample["y0"]) != 400:
                return jsonify({
                    "error": f"Sample {i}: Expected 400 pixels, got {len(sample['y0'])}"
                }), 400

            label = sample["label"]
            if not isinstance(label, int) or label < 0 or label > 9:
                return jsonify({
                    "error": f"Sample {i}: Label must be an integer between 0-9"
                }), 400

        # Convert data to matrices
        train_matrix = np.array([sample["y0"] for sample in training_data])
        train_labels = [sample["label"] for sample in training_data]
        test_matrix = np.array([sample["y0"] for sample in test_data])
        test_labels = [sample["label"] for sample in test_data]

        # Combine for indexing
        combined_matrix = np.vstack([train_matrix, test_matrix])
        combined_labels = train_labels + test_labels
        train_indices = list(range(len(training_data)))
        test_indices = list(range(len(training_data), len(training_data) + len(test_data)))

        print(f"[OPTIMIZE] Starting optimization: {len(train_indices)} train, "
              f"{len(test_indices)} test samples")
        print(f"[OPTIMIZE] Testing hidden nodes from {min_nodes} to {max_nodes} (step {step})")

        # Run optimization
        results = find_optimal_hidden_nodes(
            combined_matrix,
            combined_labels,
            train_indices,
            test_indices,
            min_nodes,
            max_nodes,
            step
        )

        # Format results
        formatted_results = [
            {"hiddenNodes": nodes, "accuracy": float(accuracy)}
            for nodes, accuracy in results
        ]

        optimal = formatted_results[0] if formatted_results else None
        configs_tested = len(formatted_results)

        print(f"[OPTIMIZE] Completed. Best: {optimal['hiddenNodes']} nodes "
              f"with {optimal['accuracy']:.4f} accuracy")

        return jsonify({
            "results": formatted_results,
            "optimal": optimal,
            "message": f"Optimization completed. Tested {configs_tested} configurations."
        }), 200

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] Optimization failed: {error_details}")
        return jsonify({"error": f"Optimization failed: {str(e)}"}), 500


def create_app():
    """Application factory for testing"""
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"Starting OCR Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
