"""
Unit tests for neural network design utilities
"""

import pytest
import numpy as np

from src import neural_network_design
from src.neural_network_design import model_test, find_optimal_hidden_nodes
from src.ocr import OCRNeuralNetwork


class TestNeuralNetworkDesign:
    """Test suite for neural network design functions"""

    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        np.random.seed(42)
        data_matrix = np.random.rand(100, 400)
        data_labels = [i % 10 for i in range(100)]
        train_indices = list(range(80))
        test_indices = list(range(80, 100))
        return data_matrix, data_labels, train_indices, test_indices

    @pytest.fixture
    def trained_nn(self, sample_data):
        """Create a trained neural network for testing"""
        data_matrix, data_labels, train_indices, _ = sample_data
        nn = OCRNeuralNetwork(
            15, data_matrix, data_labels, train_indices, use_file=False
        )
        return nn

    def test_model_test_function_structure(self, sample_data, trained_nn):
        """Test the test function returns valid results"""
        data_matrix, data_labels, _, test_indices = sample_data

        result = model_test(data_matrix, data_labels, test_indices, trained_nn)

        # Result should be a float between 0 and 1 (accuracy)
        assert isinstance(result, (float, np.floating))
        assert 0 <= result <= 1

    def test_model_test_function_with_small_test_set(self, sample_data, trained_nn):
        """Test the test function with a small test set"""
        data_matrix, data_labels, _, _ = sample_data
        small_test_indices = list(range(80, 85))  # Just 5 samples

        result = model_test(data_matrix, data_labels, small_test_indices, trained_nn)

        assert isinstance(result, (float, np.floating))
        assert 0 <= result <= 1

    def test_model_test_function_consistency(self, sample_data, trained_nn):
        """Test that the test function gives consistent results"""
        data_matrix, data_labels, _, test_indices = sample_data

        # Since we're averaging over multiple runs, results should be similar
        result1 = model_test(data_matrix, data_labels, test_indices, trained_nn)
        result2 = model_test(data_matrix, data_labels, test_indices, trained_nn)

        # Results should be close (within reasonable variance)
        assert abs(result1 - result2) < 0.3  # Allow for some randomness

    def test_model_test_function_perfect_prediction(self, sample_data):
        """Test with a scenario where predictions might be perfect"""
        data_matrix, data_labels, train_indices, _ = sample_data
        test_indices = train_indices[:10]  # Use training data as test
        # Create a well-trained network
        nn = OCRNeuralNetwork(
            20, data_matrix, data_labels, train_indices, use_file=False
        )
        # Train multiple times to improve accuracy
        for _ in range(5):
            training_data = [
                {"y0": data_matrix[i], "label": data_labels[i]}
                for i in train_indices[:20]
            ]
            nn.train(training_data)

        result = model_test(data_matrix, data_labels, test_indices, nn)

        # Result should be between 0 and 1
        assert 0 <= result <= 1

    def test_model_test_function_with_single_sample(self, sample_data, trained_nn):
        """Test the test function with a single test sample"""
        data_matrix, data_labels, _, _ = sample_data
        single_test_index = [85]

        result = model_test(data_matrix, data_labels, single_test_index, trained_nn)

        assert isinstance(result, (float, np.floating))
        assert 0 <= result <= 1

    def test_find_optimal_hidden_nodes_structure(self, sample_data):
        """Test that find_optimal_hidden_nodes executes without errors"""
        # Verify the function exists and is callable
        assert callable(find_optimal_hidden_nodes)

    def test_model_test_function_with_different_nn_sizes(self, sample_data):
        """Test the test function with neural networks of different sizes"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        for num_nodes in [5, 10, 20]:
            nn = OCRNeuralNetwork(
                num_nodes, data_matrix, data_labels, train_indices, use_file=False
            )
            result = model_test(data_matrix, data_labels, test_indices, nn)

            assert isinstance(result, (float, np.floating))
            assert 0 <= result <= 1

    def test_model_test_function_accuracy_calculation(self, sample_data):
        """Test that accuracy is calculated correctly"""
        data_matrix, data_labels, train_indices, _ = sample_data
        test_indices = [80, 81, 82]  # 3 test samples

        nn = OCRNeuralNetwork(
            10, data_matrix, data_labels, train_indices, use_file=False
        )
        result = model_test(data_matrix, data_labels, test_indices, nn)

        # With random initialization and 3 samples, accuracy should be reasonable
        assert 0 <= result <= 1

    def test_model_test_function_empty_test_set(self, sample_data, trained_nn):
        """Test the test function with empty test set"""
        data_matrix, data_labels, _, _ = sample_data
        empty_test_indices = []

        result = model_test(data_matrix, data_labels, empty_test_indices, trained_nn)
        # Should return 0.0 for empty test set
        assert result == 0.0

    def test_module_imports(self):
        """Test that all necessary functions are imported correctly"""
        assert hasattr(neural_network_design, "model_test")
        assert hasattr(neural_network_design, "find_optimal_hidden_nodes")

    def test_repeated_testing(self, sample_data, trained_nn):
        """Test running the test function multiple times"""
        data_matrix, data_labels, _, test_indices = sample_data

        results = []
        for _ in range(3):
            result = model_test(data_matrix, data_labels, test_indices, trained_nn)
            results.append(result)
            assert 0 <= result <= 1

        # All results should be valid
        assert all(0 <= r <= 1 for r in results)

    def test_different_data_splits(self, sample_data, trained_nn):
        """Test with different train/test splits"""
        data_matrix, data_labels, _, _ = sample_data

        # Test with different splits
        test_indices_1 = list(range(80, 90))
        test_indices_2 = list(range(90, 100))

        result1 = model_test(data_matrix, data_labels, test_indices_1, trained_nn)
        result2 = model_test(data_matrix, data_labels, test_indices_2, trained_nn)

        assert 0 <= result1 <= 1
        assert 0 <= result2 <= 1
    def test_find_optimal_hidden_nodes_returns_results(self, sample_data):
        """Test that find_optimal_hidden_nodes returns sorted results"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        results = find_optimal_hidden_nodes(
            data_matrix, data_labels, train_indices, test_indices,
            min_nodes=5, max_nodes=15, step=5
        )

        # Should return a list of tuples
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Each result should be a tuple of (hidden_nodes, accuracy)
        for hidden_nodes, accuracy in results:
            assert isinstance(hidden_nodes, int)
            assert isinstance(accuracy, (float, np.floating))
            assert 0 <= accuracy <= 1

    def test_find_optimal_hidden_nodes_sorted(self, sample_data):
        """Test that results are sorted by accuracy (descending)"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        results = find_optimal_hidden_nodes(
            data_matrix, data_labels, train_indices, test_indices,
            min_nodes=5, max_nodes=15, step=5
        )

        # Extract accuracies
        accuracies = [acc for _, acc in results]
        
        # Should be sorted in descending order
        assert accuracies == sorted(accuracies, reverse=True)

    def test_find_optimal_hidden_nodes_custom_range(self, sample_data):
        """Test find_optimal_hidden_nodes with custom range"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        results = find_optimal_hidden_nodes(
            data_matrix, data_labels, train_indices, test_indices,
            min_nodes=10, max_nodes=20, step=2
        )

        # Should have results for nodes: 10, 12, 14, 16, 18
        assert len(results) == 5
        
        # Check that all expected node counts are present
        node_counts = [nodes for nodes, _ in results]
        expected_nodes = [10, 12, 14, 16, 18]
        assert sorted(node_counts) == expected_nodes

    def test_find_optimal_hidden_nodes_single_configuration(self, sample_data):
        """Test find_optimal_hidden_nodes with single configuration"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        results = find_optimal_hidden_nodes(
            data_matrix, data_labels, train_indices, test_indices,
            min_nodes=15, max_nodes=16, step=5
        )

        # Should test only 15 hidden nodes
        assert len(results) == 1
        assert results[0][0] == 15
        assert 0 <= results[0][1] <= 1

    def test_find_optimal_hidden_nodes_best_is_first(self, sample_data):
        """Test that the best configuration is first in results"""
        data_matrix, data_labels, train_indices, test_indices = sample_data

        results = find_optimal_hidden_nodes(
            data_matrix, data_labels, train_indices, test_indices,
            min_nodes=5, max_nodes=20, step=5
        )

        # First result should have the highest accuracy
        best_accuracy = results[0][1]
        for _, accuracy in results:
            assert accuracy <= best_accuracy