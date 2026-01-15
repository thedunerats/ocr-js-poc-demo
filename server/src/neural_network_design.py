"""
This script tests different neural network configurations to find the optimal number
of hidden nodes.
It trains networks with varying hidden node counts and evaluates their performance.
"""

from src.ocr import OCRNeuralNetwork


def model_test(data_matrix, data_labels, test_indices, nn):
    """
    Test the neural network's accuracy

    Args:
        data_matrix: Matrix of input data
        data_labels: Corresponding labels for the data
        test_indices: Indices to use for testing
        nn: The OCRNeuralNetwork instance

    Returns:
        Average accuracy across 100 test runs
    """
    if not test_indices:
        return 0.0

    # Run fewer test iterations for faster optimization
    # (100 was overkill for small test sets)
    test_runs = 10
    avg_sum = 0
    for _ in range(test_runs):
        correct_guess_count = 0
        for i in test_indices:
            test = data_matrix[i]
            prediction = nn.predict(test)
            if data_labels[i] == prediction:
                correct_guess_count += 1

        avg_sum += correct_guess_count / float(len(test_indices))
    return avg_sum / test_runs


def find_optimal_hidden_nodes(
    data_matrix, data_labels, train_indices, test_indices, min_nodes=5, max_nodes=50, step=5
):
    """
    Try various numbers of hidden nodes and see what performs best

    Args:
        data_matrix: Matrix of input data
        data_labels: Corresponding labels for the data
        train_indices: Indices to use for training
        test_indices: Indices to use for testing
        min_nodes: Minimum number of hidden nodes to test (default: 5)
        max_nodes: Maximum number of hidden nodes to test (default: 50)
        step: Step size for testing (default: 5)

    Returns:
        List of tuples (hidden_nodes, accuracy) sorted by accuracy (best first)
    """
    print("Testing different hidden node configurations...")
    print("-" * 50)

    results = []
    # Train each configuration for a few epochs
    # Too many epochs with small datasets causes overfitting
    epochs = 3

    print(f"Training with {len(train_indices)} samples, testing with {len(test_indices)} samples")
    print(f"Each configuration will train for {epochs} epochs")

    for i in range(min_nodes, max_nodes, step):
        nn = OCRNeuralNetwork(i, data_matrix, data_labels, train_indices, False)

        # Train for additional epochs (first epoch done in __init__)
        for epoch in range(epochs - 1):
            nn._train(data_matrix, data_labels, train_indices)

        performance = model_test(data_matrix, data_labels, test_indices, nn)
        results.append((i, performance))
        print(f"{i} Hidden Nodes: {performance:.4f} (accuracy on {len(test_indices)} test samples)")

    # Sort by accuracy (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    return results


if __name__ == "__main__":
    # Example usage with dummy data
    # In a real scenario, you would load actual MNIST or similar dataset
    print("Note: This script requires actual training data to run properly.")
    print(
        "Please provide a dataset (e.g., MNIST) to test neural network configurations."
    )

    # Placeholder for demonstration
    # data_matrix = np.random.rand(1000, 400)  # 1000 samples, 400 features
    # data_labels = np.random.randint(0, 10, 1000)  # Random labels 0-9
    # train_indices = list(range(800))  # First 800 for training
    # test_indices = list(range(800, 1000))  # Last 200 for testing
    # find_optimal_hidden_nodes(data_matrix, data_labels, train_indices, test_indices)
