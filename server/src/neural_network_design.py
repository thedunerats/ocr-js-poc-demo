"""
This script tests different neural network configurations to find the optimal number
of hidden nodes.
It trains networks with varying hidden node counts and evaluates their performance.
"""
from ocr import OCRNeuralNetwork


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
    
    avg_sum = 0
    for _ in range(100):
        correct_guess_count = 0
        for i in test_indices:
            test = data_matrix[i]
            prediction = nn.predict(test)
            if data_labels[i] == prediction:
                correct_guess_count += 1

        avg_sum += (correct_guess_count / float(len(test_indices)))
    return avg_sum / 100


def find_optimal_hidden_nodes(data_matrix, data_labels, train_indices, test_indices):
    """
    Try various numbers of hidden nodes and see what performs best

    Args:
        data_matrix: Matrix of input data
        data_labels: Corresponding labels for the data
        train_indices: Indices to use for training
        test_indices: Indices to use for testing
    """
    print("Testing different hidden node configurations...")
    print("-" * 50)

    for i in range(5, 50, 5):
        nn = OCRNeuralNetwork(i, data_matrix, data_labels, train_indices, False)
        performance = test(data_matrix, data_labels, test_indices, nn)
        print(f"{i} Hidden Nodes: {performance:.4f}")


if __name__ == '__main__':
    # Example usage with dummy data
    # In a real scenario, you would load actual MNIST or similar dataset
    print("Note: This script requires actual training data to run properly.")
    print("Please provide a dataset (e.g., MNIST) to test neural network configurations.")

    # Placeholder for demonstration
    # data_matrix = np.random.rand(1000, 400)  # 1000 samples, 400 features
    # data_labels = np.random.randint(0, 10, 1000)  # Random labels 0-9
    # train_indices = list(range(800))  # First 800 for training
    # test_indices = list(range(800, 1000))  # Last 200 for testing
    # find_optimal_hidden_nodes(data_matrix, data_labels, train_indices, test_indices)
