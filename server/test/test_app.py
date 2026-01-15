"""
Unit tests for the Flask server
"""

import pytest
import json
import os
import numpy as np

from src.app import create_app
from src.ocr import OCRNeuralNetwork


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config["TESTING"] = True

    # Change NN file path to avoid conflicts
    OCRNeuralNetwork.NN_FILE_PATH = "test_ocr_neural_network.json"

    yield app

    # Cleanup
    if os.path.exists("test_ocr_neural_network.json"):
        os.remove("test_ocr_neural_network.json")


@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()


class TestFlaskServer:
    """Test suite for Flask server endpoints"""

    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "message" in data

    def test_post_endpoint_no_data(self, client):
        """Test POST endpoint with no data"""
        response = client.post("/", data="", content_type="application/json")

        assert response.status_code == 400

    def test_post_endpoint_invalid_json(self, client):
        """Test POST endpoint with invalid JSON"""
        response = client.post("/", data="not json", content_type="application/json")

        assert response.status_code == 400

    def test_train_endpoint_missing_train_array(self, client):
        """Test training endpoint without trainArray"""
        payload = {"train": True}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "trainArray" in data["error"]

    def test_train_endpoint_success(self, client):
        """Test successful training request"""
        payload = {
            "train": True,
            "trainArray": [
                {"y0": [0.5] * 400, "label": 5},
                {"y0": [0.3] * 400, "label": 3},
            ],
        }

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "message" in data

    def test_predict_endpoint_missing_image(self, client):
        """Test prediction endpoint without image"""
        payload = {"predict": True}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "image" in data["error"]

    def test_predict_endpoint_success(self, client):
        """Test successful prediction request"""
        # Create a random 400-element array (20x20 pixels)
        test_image = np.random.rand(400).tolist()

        payload = {"predict": True, "image": test_image}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "type" in data
        assert data["type"] == "test"
        assert "result" in data
        assert 0 <= data["result"] <= 9

    def test_predict_endpoint_with_zeros(self, client):
        """Test prediction with all zeros"""
        payload = {"predict": True, "image": [0] * 400}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "result" in data
        assert isinstance(data["result"], int)

    def test_predict_endpoint_with_ones(self, client):
        """Test prediction with all ones"""
        payload = {"predict": True, "image": [1] * 400}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "result" in data

    def test_invalid_request_type(self, client):
        """Test request without train or predict"""
        payload = {"invalid": True}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_cors_headers(self, client):
        """Test that CORS headers are present"""
        response = client.get("/health")

        assert "Access-Control-Allow-Origin" in response.headers

    def test_train_then_predict(self, client):
        """Test training followed by prediction"""
        # First train
        train_payload = {
            "train": True,
            "trainArray": [
                {"y0": [0.8] * 400, "label": 7},
                {"y0": [0.2] * 400, "label": 2},
                {"y0": [0.5] * 400, "label": 5},
            ],
        }

        train_response = client.post(
            "/", data=json.dumps(train_payload), content_type="application/json"
        )
        assert train_response.status_code == 200

        # Then predict
        predict_payload = {"predict": True, "image": [0.5] * 400}

        predict_response = client.post(
            "/", data=json.dumps(predict_payload), content_type="application/json"
        )
        assert predict_response.status_code == 200
        data = json.loads(predict_response.data)
        assert 0 <= data["result"] <= 9

    def test_multiple_predictions(self, client):
        """Test making multiple predictions"""
        for _ in range(5):
            payload = {"predict": True, "image": np.random.rand(400).tolist()}

            response = client.post(
                "/", data=json.dumps(payload), content_type="application/json"
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert "result" in data

    def test_predict_with_invalid_image_size(self, client):
        """Test prediction with wrong image size"""
        payload = {"predict": True, "image": [0.5] * 100}  # Wrong size, should be 400

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        # Should handle error gracefully
        assert response.status_code in [400, 500]

    def test_empty_train_array(self, client):
        """Test training with empty array"""
        payload = {"train": True, "trainArray": []}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        # Empty array is falsy, should return error
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_train_missing_y0_field(self, client):
        """Test training with missing y0 field"""
        payload = {"train": True, "trainArray": [{"label": 5}]}  # Missing y0

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "y0" in data["error"].lower()

    def test_train_missing_label_field(self, client):
        """Test training with missing label field"""
        payload = {"train": True, "trainArray": [{"y0": [0.5] * 400}]}  # Missing label

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "label" in data["error"].lower()

    def test_train_invalid_array_size(self, client):
        """Test training with wrong array size"""
        payload = {
            "train": True,
            "trainArray": [{"y0": [0.5] * 100, "label": 5}],  # Wrong size
        }

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "400 pixels" in data["error"] or "400" in data["error"]

    def test_train_invalid_label_range(self, client):
        """Test training with label outside 0-9 range"""
        payload = {"train": True, "trainArray": [{"y0": [0.5] * 400, "label": 15}]}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "0-9" in data["error"] or "label" in data["error"].lower()

    def test_train_negative_label(self, client):
        """Test training with negative label"""
        payload = {"train": True, "trainArray": [{"y0": [0.5] * 400, "label": -1}]}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_train_non_integer_label(self, client):
        """Test training with non-integer label"""
        payload = {"train": True, "trainArray": [{"y0": [0.5] * 400, "label": "five"}]}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_predict_wrong_array_size(self, client):
        """Test prediction with wrong array size"""
        payload = {"predict": True, "image": [0.5] * 100}  # Wrong size

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "400" in data["error"]

    def test_predict_non_array_image(self, client):
        """Test prediction with non-array image"""
        payload = {"predict": True, "image": "not an array"}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "array" in data["error"].lower()

    def test_predict_non_numeric_values(self, client):
        """Test prediction with non-numeric values in array"""
        image = [0.5] * 399 + ["invalid"]
        payload = {"predict": True, "image": image}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "numeric" in data["error"].lower()

    def test_train_non_numeric_pixel_values(self, client):
        """Test training with non-numeric pixel values"""
        # Create valid training data except one sample has non-numeric pixel
        train_array = [
            {"y0": [0.5] * 400, "label": 1},
            {"y0": [0.3] * 400, "label": 2},
            {"y0": [0.5] * 399 + [None], "label": 3},  # Invalid pixel value
        ]
        payload = {"train": True, "trainArray": train_array}

        response = client.post(
            "/", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "sample 2" in data["error"].lower()  # Third sample (index 2)
        assert "pixel 399" in data["error"].lower()  # Last pixel
        assert "invalid value" in data["error"].lower()

class TestOptimizeEndpoint:
    """Test suite for the /optimize endpoint"""

    def test_optimize_endpoint_success(self, client):
        """Test successful optimization with valid data"""
        # Create training and test data
        training_data = [
            {"y0": [0.5] * 400, "label": i % 10}
            for i in range(20)  # 20 training samples
        ]
        test_data = [
            {"y0": [0.3] * 400, "label": i % 10}
            for i in range(10)  # 10 test samples
        ]

        payload = {
            "trainingData": training_data,
            "testData": test_data,
            "minNodes": 5,
            "maxNodes": 15,
            "step": 5
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "results" in data
        assert "optimal" in data
        assert "message" in data
        assert isinstance(data["results"], list)
        assert len(data["results"]) > 0
        assert "hiddenNodes" in data["optimal"]
        assert "accuracy" in data["optimal"]

    def test_optimize_endpoint_missing_training_data(self, client):
        """Test optimization with missing trainingData"""
        payload = {
            "testData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "trainingData" in data["error"]

    def test_optimize_endpoint_missing_test_data(self, client):
        """Test optimization with missing testData"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "testData" in data["error"]

    def test_optimize_endpoint_empty_training_data(self, client):
        """Test optimization with empty trainingData"""
        payload = {
            "trainingData": [],
            "testData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "cannot be empty" in data["error"]

    def test_optimize_endpoint_empty_test_data(self, client):
        """Test optimization with empty testData"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 1}],
            "testData": []
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "cannot be empty" in data["error"]

    def test_optimize_endpoint_invalid_min_nodes(self, client):
        """Test optimization with invalid minNodes"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 1}],
            "testData": [{"y0": [0.5] * 400, "label": 1}],
            "minNodes": 0
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "minNodes" in data["error"]

    def test_optimize_endpoint_invalid_max_nodes(self, client):
        """Test optimization with maxNodes <= minNodes"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 1}],
            "testData": [{"y0": [0.5] * 400, "label": 1}],
            "minNodes": 10,
            "maxNodes": 5
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "maxNodes" in data["error"]

    def test_optimize_endpoint_invalid_step(self, client):
        """Test optimization with invalid step"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 1}],
            "testData": [{"y0": [0.5] * 400, "label": 1}],
            "step": 0
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "step" in data["error"]

    def test_optimize_endpoint_invalid_data_format(self, client):
        """Test optimization with invalid data format"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400}],  # Missing label
            "testData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "label" in data["error"].lower()

    def test_optimize_endpoint_invalid_array_size(self, client):
        """Test optimization with wrong array size"""
        payload = {
            "trainingData": [{"y0": [0.5] * 100, "label": 1}],  # Wrong size
            "testData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "400 pixels" in data["error"]

    def test_optimize_endpoint_invalid_label_range(self, client):
        """Test optimization with invalid label"""
        payload = {
            "trainingData": [{"y0": [0.5] * 400, "label": 10}],  # Invalid label
            "testData": [{"y0": [0.5] * 400, "label": 1}]
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "0-9" in data["error"]

    def test_optimize_endpoint_default_parameters(self, client):
        """Test optimization with default parameters"""
        training_data = [
            {"y0": [0.5] * 400, "label": i % 10}
            for i in range(20)
        ]
        test_data = [
            {"y0": [0.3] * 400, "label": i % 10}
            for i in range(10)
        ]

        payload = {
            "trainingData": training_data,
            "testData": test_data
            # No minNodes, maxNodes, step - should use defaults
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "results" in data
        assert len(data["results"]) > 0

    def test_optimize_endpoint_results_sorted(self, client):
        """Test that optimization results are sorted by accuracy"""
        training_data = [
            {"y0": [0.5] * 400, "label": i % 10}
            for i in range(20)
        ]
        test_data = [
            {"y0": [0.3] * 400, "label": i % 10}
            for i in range(10)
        ]

        payload = {
            "trainingData": training_data,
            "testData": test_data,
            "minNodes": 5,
            "maxNodes": 20,
            "step": 5
        }

        response = client.post(
            "/optimize", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        results = data["results"]
        
        # Check that results are sorted by accuracy (descending)
        accuracies = [r["accuracy"] for r in results]
        assert accuracies == sorted(accuracies, reverse=True)
        
        # Check that optimal is the best result
        assert data["optimal"] == results[0]

    def test_optimize_endpoint_no_json(self, client):
        """Test optimization endpoint with no JSON data"""
        response = client.post("/optimize", data="", content_type="application/json")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data