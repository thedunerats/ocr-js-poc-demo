"""
Unit tests for the Flask server
"""
import pytest
import json
import sys
import os
import numpy as np

from src.app import create_app
from src.ocr import OCRNeuralNetwork

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config['TESTING'] = True

    # Change NN file path to avoid conflicts
    OCRNeuralNetwork.NN_FILE_PATH = 'test_ocr_neural_network.json'

    yield app

    # Cleanup
    if os.path.exists('test_ocr_neural_network.json'):
        os.remove('test_ocr_neural_network.json')


@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()


class TestFlaskServer:
    """Test suite for Flask server endpoints"""

    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data

    def test_post_endpoint_no_data(self, client):
        """Test POST endpoint with no data"""
        response = client.post('/',
                              data=None,
                              content_type='application/json')
    
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_post_endpoint_invalid_json(self, client):
        """Test POST endpoint with invalid JSON"""
        response = client.post('/',
                              data='not json',
                              content_type='application/json')

        # Flask returns 400 for invalid JSON
        assert response.status_code == 400

    def test_train_endpoint_missing_train_array(self, client):
        """Test training endpoint without trainArray"""
        payload = {'train': True}

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'trainArray' in data['error']

    def test_train_endpoint_success(self, client):
        """Test successful training request"""
        payload = {
            'train': True,
            'trainArray': [
                {'y0': [0.5] * 400, 'label': 5},
                {'y0': [0.3] * 400, 'label': 3}
            ]
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'message' in data

    def test_predict_endpoint_missing_image(self, client):
        """Test prediction endpoint without image"""
        payload = {'predict': True}

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'image' in data['error']

    def test_predict_endpoint_success(self, client):
        """Test successful prediction request"""
        # Create a random 400-element array (20x20 pixels)
        test_image = np.random.rand(400).tolist()

        payload = {
            'predict': True,
            'image': test_image
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'type' in data
        assert data['type'] == 'test'
        assert 'result' in data
        assert 0 <= data['result'] <= 9

    def test_predict_endpoint_with_zeros(self, client):
        """Test prediction with all zeros"""
        payload = {
            'predict': True,
            'image': [0] * 400
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert isinstance(data['result'], int)

    def test_predict_endpoint_with_ones(self, client):
        """Test prediction with all ones"""
        payload = {
            'predict': True,
            'image': [1] * 400
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data

    def test_invalid_request_type(self, client):
        """Test request without train or predict"""
        payload = {'invalid': True}
        
        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_cors_headers(self, client):
        """Test that CORS headers are present"""
        response = client.get('/health')

        assert 'Access-Control-Allow-Origin' in response.headers

    def test_train_then_predict(self, client):
        """Test training followed by prediction"""
        # First train
        train_payload = {
            'train': True,
            'trainArray': [
                {'y0': [0.8] * 400, 'label': 7},
                {'y0': [0.2] * 400, 'label': 2},
                {'y0': [0.5] * 400, 'label': 5}
            ]
        }

        train_response = client.post('/',
                                    data=json.dumps(train_payload),
                                    content_type='application/json')
        assert train_response.status_code == 200

        # Then predict
        predict_payload = {
            'predict': True,
            'image': [0.5] * 400
        }

        predict_response = client.post('/',
                                      data=json.dumps(predict_payload),
                                      content_type='application/json')
        assert predict_response.status_code == 200
        data = json.loads(predict_response.data)
        assert 0 <= data['result'] <= 9

    def test_multiple_predictions(self, client):
        """Test making multiple predictions"""
        for _ in range(5):
            payload = {
                'predict': True,
                'image': np.random.rand(400).tolist()
            }

            response = client.post('/',
                                  data=json.dumps(payload),
                                  content_type='application/json')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'result' in data

    def test_predict_with_invalid_image_size(self, client):
        """Test prediction with wrong image size"""
        payload = {
            'predict': True,
            'image': [0.5] * 100  # Wrong size, should be 400
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        # Should handle error gracefully
        assert response.status_code in [400, 500]

    def test_empty_train_array(self, client):
        """Test training with empty array"""
        payload = {
            'train': True,
            'trainArray': []
        }

        response = client.post('/',
                              data=json.dumps(payload),
                              content_type='application/json')

        # Empty array is falsy, should return error
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
