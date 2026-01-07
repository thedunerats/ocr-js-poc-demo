"""
Unit tests for the OCRNeuralNetwork class
"""
import pytest
import numpy as np
import json
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ocr import OCRNeuralNetwork


class TestOCRNeuralNetwork:
    """Test suite for OCRNeuralNetwork"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data"""
        np.random.seed(42)
        data_matrix = np.random.rand(50, 400)
        data_labels = [i % 10 for i in range(50)]
        training_indices = list(range(40))
        return data_matrix, data_labels, training_indices
    
    @pytest.fixture
    def nn_instance(self, sample_data, tmp_path):
        """Create a neural network instance for testing"""
        data_matrix, data_labels, training_indices = sample_data
        
        # Change to temp directory to avoid file conflicts
        original_path = OCRNeuralNetwork.NN_FILE_PATH
        OCRNeuralNetwork.NN_FILE_PATH = str(tmp_path / 'test_nn.json')
        
        nn = OCRNeuralNetwork(15, data_matrix, data_labels, training_indices, use_file=False)
        
        yield nn
        
        # Cleanup
        OCRNeuralNetwork.NN_FILE_PATH = original_path
        if os.path.exists(str(tmp_path / 'test_nn.json')):
            os.remove(str(tmp_path / 'test_nn.json'))
    
    def test_initialization(self, sample_data):
        """Test neural network initialization"""
        data_matrix, data_labels, training_indices = sample_data
        nn = OCRNeuralNetwork(20, data_matrix, data_labels, training_indices, use_file=False)
        
        assert nn.num_hidden_nodes == 20
        assert len(nn.theta1) == 20
        assert len(nn.theta2) == 10
        assert len(nn.input_layer_bias) == 20
        assert len(nn.hidden_layer_bias) == 10
    
    def test_rand_initialize_weights(self, nn_instance):
        """Test weight initialization"""
        weights = nn_instance._rand_initialize_weights(10, 5)
        
        assert len(weights) == 5
        assert all(isinstance(w, np.ndarray) for w in weights)
        assert all(len(w) == 10 for w in weights)
        
        # Check weights are in expected range [-0.06, 0.06]
        for weight in weights:
            assert all(-0.06 <= w <= 0.06 for w in weight)
    
    def test_sigmoid_scalar(self, nn_instance):
        """Test sigmoid activation function"""
        assert nn_instance._sigmoid_scalar(0) == 0.5
        assert 0 < nn_instance._sigmoid_scalar(-5) < 0.5
        assert 0.5 < nn_instance._sigmoid_scalar(5) < 1
        
        # Test extreme values
        assert nn_instance._sigmoid_scalar(-100) < 0.01
        assert nn_instance._sigmoid_scalar(100) > 0.99
    
    def test_sigmoid_vectorized(self, nn_instance):
        """Test vectorized sigmoid function"""
        z = np.array([[0, 1, -1], [2, -2, 0]])
        result = nn_instance.sigmoid(z)
        
        assert result.shape == z.shape
        assert np.all((result >= 0) & (result <= 1))
        assert result[0, 0] == 0.5  # sigmoid(0) = 0.5
    
    def test_sigmoid_prime(self, nn_instance):
        """Test sigmoid derivative"""
        z = np.array([[0, 1, -1]])
        result = nn_instance.sigmoid_prime(z)
        
        assert result.shape == z.shape
        assert np.all(result >= 0)  # Derivative should be positive
        assert result[0, 0] == 0.25  # sigmoid'(0) = 0.25
    
    def test_predict(self, nn_instance):
        """Test prediction functionality"""
        test_input = np.random.rand(400)
        prediction = nn_instance.predict(test_input)
        
        assert isinstance(prediction, (int, np.integer))
        assert 0 <= prediction <= 9
    
    def test_train(self, nn_instance):
        """Test training functionality"""
        training_data = [
            {'y0': np.random.rand(400), 'label': 5},
            {'y0': np.random.rand(400), 'label': 3}
        ]
        
        # Store original weights
        original_theta1 = [np.array(t) for t in nn_instance.theta1]
        
        nn_instance.train(training_data)
        
        # Check that weights have been updated
        weights_changed = any(
            not np.array_equal(original_theta1[i], nn_instance.theta1[i])
            for i in range(len(original_theta1))
        )
        assert weights_changed
    
    def test_save_and_load(self, nn_instance, tmp_path):
        """Test saving and loading neural network"""
        # Change file path to temp directory
        nn_instance.NN_FILE_PATH = str(tmp_path / 'test_save_nn.json')
        nn_instance._use_file = True
        
        # Save the network
        nn_instance.save()
        assert os.path.exists(nn_instance.NN_FILE_PATH)
        
        # Check JSON structure
        with open(nn_instance.NN_FILE_PATH, 'r') as f:
            saved_data = json.load(f)
        
        assert 'theta1' in saved_data
        assert 'theta2' in saved_data
        assert 'b1' in saved_data
        assert 'b2' in saved_data
        
        # Store original weights
        original_theta1 = [np.array(t) for t in nn_instance.theta1]
        original_theta2 = [np.array(t) for t in nn_instance.theta2]
        
        # Modify weights
        nn_instance.theta1 = nn_instance._rand_initialize_weights(400, nn_instance.num_hidden_nodes)
        
        # Load weights back
        nn_instance._load()
        
        # Verify loaded weights match original
        for i in range(len(original_theta1)):
            assert np.allclose(nn_instance.theta1[i], original_theta1[i])
        for i in range(len(original_theta2)):
            assert np.allclose(nn_instance.theta2[i], original_theta2[i])
        
        # Cleanup
        os.remove(nn_instance.NN_FILE_PATH)
    
    def test_save_when_use_file_false(self, nn_instance, tmp_path):
        """Test that save does nothing when use_file is False"""
        nn_instance.NN_FILE_PATH = str(tmp_path / 'should_not_exist.json')
        nn_instance._use_file = False
        
        nn_instance.save()
        assert not os.path.exists(nn_instance.NN_FILE_PATH)
    
    def test_load_when_use_file_false(self, nn_instance):
        """Test that load does nothing when use_file is False"""
        nn_instance._use_file = False
        original_theta1 = [np.array(t) for t in nn_instance.theta1]
        
        nn_instance._load()
        
        # Weights should be unchanged
        for i in range(len(original_theta1)):
            assert np.array_equal(nn_instance.theta1[i], original_theta1[i])
    
    def test_predict_consistency(self, nn_instance):
        """Test that predictions are consistent for the same input"""
        test_input = np.random.rand(400)
        
        prediction1 = nn_instance.predict(test_input)
        prediction2 = nn_instance.predict(test_input)
        
        assert prediction1 == prediction2
    
    def test_different_hidden_nodes(self, sample_data):
        """Test initialization with different numbers of hidden nodes"""
        data_matrix, data_labels, training_indices = sample_data
        
        for num_nodes in [5, 10, 20, 30]:
            nn = OCRNeuralNetwork(num_nodes, data_matrix, data_labels, 
                                 training_indices, use_file=False)
            assert nn.num_hidden_nodes == num_nodes
            assert len(nn.theta1) == num_nodes
