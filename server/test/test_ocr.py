"""
Unit tests for the OCRNeuralNetwork class
"""

import pytest
import numpy as np
import json
import os
from src.ocr import OCRNeuralNetwork


class TestOCRNeuralNetwork:
    """Test suite for OCRNeuralNetwork"""

    @pytest.fixture
    def sample_data(self):
        """Create sample training data"""
        np.random.seed(42)
        data_matrix = np.random.rand(50, 784)
        data_labels = [i % 10 for i in range(50)]
        training_indices = list(range(40))
        return data_matrix, data_labels, training_indices

    @pytest.fixture
    def nn_instance(self, sample_data, tmp_path):
        """Create a neural network instance for testing"""
        data_matrix, data_labels, training_indices = sample_data

        # Change to temp directory to avoid file conflicts
        original_path = OCRNeuralNetwork.NN_FILE_PATH
        OCRNeuralNetwork.NN_FILE_PATH = str(tmp_path / "test_nn.json")

        nn = OCRNeuralNetwork(
            15, data_matrix, data_labels, training_indices, use_file=False
        )

        yield nn

        # Cleanup
        OCRNeuralNetwork.NN_FILE_PATH = original_path
        if os.path.exists(str(tmp_path / "test_nn.json")):
            os.remove(str(tmp_path / "test_nn.json"))

    def test_initialization(self, sample_data):
        """Test neural network initialization"""
        data_matrix, data_labels, training_indices = sample_data
        nn = OCRNeuralNetwork(
            20, data_matrix, data_labels, training_indices, use_file=False
        )

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
        test_input = np.random.rand(784)
        prediction = nn_instance.predict(test_input)

        assert isinstance(prediction, (int, np.integer))
        assert 0 <= prediction <= 9

    def test_train(self, nn_instance):
        """Test training functionality"""
        training_data = [
            {"y0": np.random.rand(784), "label": 5},
            {"y0": np.random.rand(784), "label": 3},
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
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_save_nn.json")
        nn_instance._use_file = True

        # Save the network
        nn_instance.save()
        assert os.path.exists(nn_instance.NN_FILE_PATH)

        # Check JSON structure
        with open(nn_instance.NN_FILE_PATH, "r") as f:
            saved_data = json.load(f)

        assert "theta1" in saved_data
        assert "theta2" in saved_data
        assert "b1" in saved_data
        assert "b2" in saved_data

        # Store original weights and biases
        original_theta1 = [np.array(t) for t in nn_instance.theta1]
        original_theta2 = [np.array(t) for t in nn_instance.theta2]
        original_b1 = [np.array(b) for b in nn_instance.input_layer_bias]
        original_b2 = [np.array(b) for b in nn_instance.hidden_layer_bias]

        # Modify weights
        nn_instance.theta1 = nn_instance._rand_initialize_weights(
            784, nn_instance.num_hidden_nodes
        )
        nn_instance.theta2 = nn_instance._rand_initialize_weights(
            nn_instance.num_hidden_nodes, 10
        )

        # Load weights back
        nn_instance._load()

        # Verify loaded weights match original
        for i in range(len(original_theta1)):
            assert np.allclose(nn_instance.theta1[i], original_theta1[i])
        for i in range(len(original_theta2)):
            assert np.allclose(nn_instance.theta2[i], original_theta2[i])
        for i in range(len(original_b1)):
            assert np.allclose(nn_instance.input_layer_bias[i], original_b1[i])
        for i in range(len(original_b2)):
            assert np.allclose(nn_instance.hidden_layer_bias[i], original_b2[i])

    def test_save_when_use_file_false(self, nn_instance, tmp_path):
        """Test that save does nothing when use_file is False"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "should_not_exist.json")
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
        test_input = np.random.rand(784)

        prediction1 = nn_instance.predict(test_input)
        prediction2 = nn_instance.predict(test_input)

        assert prediction1 == prediction2

    def test_different_hidden_nodes(self, sample_data):
        """Test initialization with different numbers of hidden nodes"""
        data_matrix, data_labels, training_indices = sample_data

        for num_nodes in [5, 10, 20, 30]:
            nn = OCRNeuralNetwork(
                num_nodes, data_matrix, data_labels, training_indices, use_file=False
            )
            assert nn.num_hidden_nodes == num_nodes
            assert len(nn.theta1) == num_nodes

    def test_save_creates_backup(self, nn_instance, tmp_path):
        """Test that saving creates a backup of the existing file"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_backup.json")
        nn_instance._use_file = True

        # First save - no backup should be created
        nn_instance.save()
        assert os.path.exists(nn_instance.NN_FILE_PATH)
        backups = nn_instance.list_backups()
        assert len(backups) == 0

        # Second save - backup should be created
        nn_instance.save()
        backups = nn_instance.list_backups()
        assert len(backups) == 1
        assert backups[0][1].startswith(nn_instance.NN_FILE_PATH + ".backup.")

    def test_backup_cleanup(self, nn_instance, tmp_path):
        """Test that old backups are cleaned up"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_cleanup.json")
        nn_instance._use_file = True

        # Create multiple saves with max_backups=3
        for i in range(6):
            nn_instance.save(max_backups=3)
            # Small delay to ensure different timestamps
            import time

            time.sleep(0.01)

        # Should only have 3 backups
        backups = nn_instance.list_backups()
        assert len(backups) <= 3

    def test_restore_from_backup(self, nn_instance, tmp_path):
        """Test restoring neural network from backup"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_restore.json")
        nn_instance._use_file = True

        # Save initial state
        nn_instance.save()
        original_theta1 = [np.array(t) for t in nn_instance.theta1]

        # Modify and save again (creates backup)
        nn_instance.theta1 = nn_instance._rand_initialize_weights(
            784, nn_instance.num_hidden_nodes
        )
        nn_instance.save()

        # Restore from backup (index 0 = most recent backup)
        result = nn_instance.restore_from_backup(backup_index=0)
        assert result is True

        # Verify weights match original
        for i in range(len(original_theta1)):
            assert np.allclose(nn_instance.theta1[i], original_theta1[i])

    def test_restore_with_no_backups(self, nn_instance, tmp_path):
        """Test restore returns False when no backups exist"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_no_backup.json")
        nn_instance._use_file = True

        result = nn_instance.restore_from_backup()
        assert result is False

    def test_train_with_empty_array(self, nn_instance):
        """Test that training with empty array raises error"""
        with pytest.raises(ValueError, match="empty"):
            nn_instance.train([])

    def test_train_with_invalid_array_size(self, nn_instance):
        """Test training with wrong input size"""
        invalid_data = [{"y0": [0.5] * 100, "label": 5}]  # Wrong size

        with pytest.raises(ValueError, match="784"):
            nn_instance.train(invalid_data)

    def test_train_with_missing_fields(self, nn_instance):
        """Test training with missing required fields"""
        # Missing y0
        with pytest.raises(ValueError, match="y0"):
            nn_instance.train([{"label": 5}])

        # Missing label
        with pytest.raises(ValueError, match="label"):
            nn_instance.train([{"y0": [0.5] * 784}])

    def test_train_with_invalid_label(self, nn_instance):
        """Test training with invalid label values"""
        # Label too high
        with pytest.raises(ValueError, match="0-9"):
            nn_instance.train([{"y0": [0.5] * 784, "label": 15}])

        # Negative label
        with pytest.raises(ValueError, match="0-9"):
            nn_instance.train([{"y0": [0.5] * 784, "label": -1}])

    def test_train_with_non_numeric_data(self, nn_instance):
        """Test training with non-numeric input data"""
        invalid_data = [{"y0": ["a"] * 784, "label": 5}]

        with pytest.raises((ValueError, RuntimeError)):
            nn_instance.train(invalid_data)

    def test_predict_with_wrong_size(self, nn_instance):
        """Test prediction with wrong input size"""
        with pytest.raises(ValueError, match="784"):
            nn_instance.predict([0.5] * 100)

    def test_predict_with_non_numeric(self, nn_instance):
        """Test prediction with non-numeric values"""
        with pytest.raises((ValueError, RuntimeError)):
            nn_instance.predict(["invalid"] * 784)

    def test_predict_with_none(self, nn_instance):
        """Test prediction with None input"""
        with pytest.raises((ValueError, TypeError, RuntimeError)):
            nn_instance.predict(None)

    def test_train_multiple_samples_with_one_invalid(self, nn_instance):
        """Test that training fails correctly when one sample is invalid"""
        mixed_data = [
            {"y0": [0.5] * 784, "label": 5},  # Valid
            {"y0": [0.3] * 100, "label": 3},  # Invalid size
        ]

        with pytest.raises(ValueError, match="sample 1"):
            nn_instance.train(mixed_data)

    def test_train_with_boundary_labels(self, nn_instance):
        """Test training with boundary label values (0 and 9)"""
        # Should succeed with labels 0 and 9
        valid_data = [
            {"y0": [0.5] * 784, "label": 0},
            {"y0": [0.8] * 784, "label": 9},
        ]

        # Should not raise any errors
        nn_instance.train(valid_data)

    def test_predict_with_extreme_values(self, nn_instance, tmp_path):
        """Test prediction with extreme numeric values"""
        # Very large values
        result1 = nn_instance.predict([1000.0] * 784)
        assert 0 <= result1 <= 9

        # Very small values
        result2 = nn_instance.predict([-1000.0] * 784)
        assert 0 <= result2 <= 9

        # Mixed extreme values (properly generate 784 elements)
        result3 = nn_instance.predict([1e10 if i % 2 == 0 else -1e10 for i in range(784)])
        assert 0 <= result3 <= 9
        """Test that list_backups returns backups sorted by most recent first"""
        nn_instance.NN_FILE_PATH = str(tmp_path / "test_sorted.json")
        nn_instance._use_file = True

        # Create multiple saves
        nn_instance.save()
        import time

        time.sleep(0.01)
        nn_instance.save()
        time.sleep(0.01)
        nn_instance.save()

        backups = nn_instance.list_backups()
        assert len(backups) == 2  # First save has no backup

        # Verify sorted by timestamp (newest first)
        if len(backups) > 1:
            assert backups[0][0] > backups[1][0]
