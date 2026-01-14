import numpy as np
from datetime import datetime
import math
import json
import os
import shutil


class OCRNeuralNetwork:
    NN_FILE_PATH = "ocr_neural_network.json"
    LEARNING_RATE = 0.1

    def __init__(
        self,
        num_hidden_nodes,
        data_matrix,
        data_labels,
        training_indices,
        use_file=True,
    ):
        self.num_hidden_nodes = num_hidden_nodes
        self._use_file = use_file

        # Initialize weights
        self.theta1 = self._rand_initialize_weights(400, num_hidden_nodes)
        self.theta2 = self._rand_initialize_weights(num_hidden_nodes, 10)
        self.input_layer_bias = self._rand_initialize_weights(1, num_hidden_nodes)
        self.hidden_layer_bias = self._rand_initialize_weights(1, 10)

        # Try to load saved weights
        if use_file and os.path.isfile(self.NN_FILE_PATH):
            self._load()
        else:
            # Train the network
            self._train(data_matrix, data_labels, training_indices)
            self.save()

    def _rand_initialize_weights(self, size_in, size_out):
        """Initialize weights randomly"""
        return [((x * 0.12) - 0.06) for x in np.random.rand(size_out, size_in)]

    def _sigmoid_scalar(self, z):
        """The sigmoid activation function. Operates on scalars."""
        return 1 / (1 + math.e**-z)

    def sigmoid(self, z):
        """Vectorized sigmoid function"""
        return np.vectorize(self._sigmoid_scalar)(z)

    def sigmoid_prime(self, z):
        """Derivative of sigmoid function"""
        return np.multiply(self.sigmoid(z), 1 - self.sigmoid(z))

    def _train(self, data_matrix, data_labels, training_indices):
        """Train the neural network using backpropagation"""
        for i in range(len(training_indices)):
            data_index = training_indices[i]
            data = {"y0": data_matrix[data_index], "label": data_labels[data_index]}

            # Forward propagation
            y1 = np.dot(np.array(self.theta1), np.array(data["y0"]).reshape(-1, 1))
            sum1 = y1 + np.array(self.input_layer_bias).reshape(-1, 1)
            y1 = self.sigmoid(sum1)

            y2 = np.dot(np.array(self.theta2), y1)
            y2 = np.add(y2, np.array(self.hidden_layer_bias).reshape(-1, 1))
            y2 = self.sigmoid(y2)

            # Backpropagation
            actual_vals = [0] * 10
            actual_vals[data["label"]] = 1
            output_errors = np.array(actual_vals).reshape(-1, 1) - y2
            hidden_errors = np.multiply(
                np.dot(np.array(self.theta2).T, output_errors), self.sigmoid_prime(sum1)
            )

            # Update weights
            self.theta1 += self.LEARNING_RATE * np.dot(
                hidden_errors, np.array(data["y0"]).reshape(1, -1)
            )
            self.theta2 += self.LEARNING_RATE * np.dot(output_errors, y1.T)
            self.hidden_layer_bias += self.LEARNING_RATE * output_errors
            self.input_layer_bias += self.LEARNING_RATE * hidden_errors

    def train(self, training_data_array):
        """Train the network with new data"""
        for data in training_data_array:
            # Forward propagation
            y1 = np.dot(np.array(self.theta1), np.array(data["y0"]).reshape(-1, 1))
            sum1 = y1 + np.array(self.input_layer_bias).reshape(-1, 1)
            y1 = self.sigmoid(sum1)

            y2 = np.dot(np.array(self.theta2), y1)
            y2 = np.add(y2, np.array(self.hidden_layer_bias).reshape(-1, 1))
            y2 = self.sigmoid(y2)

            # Backpropagation
            actual_vals = [0] * 10
            actual_vals[data["label"]] = 1
            output_errors = np.array(actual_vals).reshape(-1, 1) - y2
            hidden_errors = np.multiply(
                np.dot(np.array(self.theta2).T, output_errors), self.sigmoid_prime(sum1)
            )

            # Update weights
            self.theta1 += self.LEARNING_RATE * np.dot(
                hidden_errors, np.array(data["y0"]).reshape(1, -1)
            )
            self.theta2 += self.LEARNING_RATE * np.dot(output_errors, y1.T)
            self.hidden_layer_bias += self.LEARNING_RATE * output_errors
            self.input_layer_bias += self.LEARNING_RATE * hidden_errors

    def predict(self, test):
        """Predict the digit from input data"""
        y1 = np.dot(np.array(self.theta1), np.array(test).reshape(-1, 1))
        y1 = y1 + np.array(self.input_layer_bias).reshape(-1, 1)
        y1 = self.sigmoid(y1)

        y2 = np.dot(np.array(self.theta2), y1)
        y2 = np.add(y2, np.array(self.hidden_layer_bias).reshape(-1, 1))
        y2 = self.sigmoid(y2)

        results = y2.flatten().tolist()
        return results.index(max(results))

    def save(self, max_backups=5):
        """Save the neural network to file with backup protection

        Args:
            max_backups: Maximum number of backup files to keep (default: 5)
        """
        if not self._use_file:
            return

        # Ensure directory exists (only if path contains a directory)
        dir_path = os.path.dirname(self.NN_FILE_PATH)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # Create backup if file exists
        if os.path.exists(self.NN_FILE_PATH):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            backup_path = f"{self.NN_FILE_PATH}.backup.{timestamp}"
            shutil.copy2(self.NN_FILE_PATH, backup_path)

            # Clean up old backups
            self._cleanup_old_backups(max_backups)

        json_neural_network = {
            "theta1": [
                w.tolist() if isinstance(w, np.ndarray) else w for w in self.theta1
            ],
            "theta2": [
                w.tolist() if isinstance(w, np.ndarray) else w for w in self.theta2
            ],
            "b1": [
                w.tolist() if isinstance(w, np.ndarray) else w
                for w in self.input_layer_bias
            ],
            "b2": [
                w.tolist() if isinstance(w, np.ndarray) else w
                for w in self.hidden_layer_bias
            ],
        }

        with open(self.NN_FILE_PATH, "w") as nnFile:
            json.dump(json_neural_network, nnFile)

    def _cleanup_old_backups(self, max_backups):
        """Remove old backup files, keeping only the most recent max_backups

        Args:
            max_backups: Maximum number of backup files to keep
        """
        backup_dir = os.path.dirname(self.NN_FILE_PATH)
        backup_prefix = os.path.basename(self.NN_FILE_PATH) + ".backup."

        # Find all backup files
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith(backup_prefix):
                backup_path = os.path.join(backup_dir, filename)
                backups.append((os.path.getmtime(backup_path), backup_path))

        # Sort by modification time (oldest first)
        backups.sort()

        # Remove oldest backups if we exceed max_backups
        while len(backups) > max_backups:
            _, old_backup = backups.pop(0)
            os.remove(old_backup)

    def restore_from_backup(self, backup_index=0):
        """Restore neural network from a backup file

        Args:
            backup_index: Index of backup to restore (0 = most recent, 1 = second most recent, etc.)

        Returns:
            bool: True if restore successful, False otherwise
        """
        if not self._use_file:
            return False

        backup_dir = os.path.dirname(self.NN_FILE_PATH)
        backup_prefix = os.path.basename(self.NN_FILE_PATH) + ".backup."

        # Find all backup files
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith(backup_prefix):
                backup_path = os.path.join(backup_dir, filename)
                backups.append((os.path.getmtime(backup_path), backup_path))

        # Sort by modification time (newest first)
        backups.sort(reverse=True)

        if backup_index >= len(backups):
            return False

        # Restore the selected backup
        _, backup_path = backups[backup_index]
        shutil.copy2(backup_path, self.NN_FILE_PATH)

        # Reload the restored weights
        self._load()
        return True

    def list_backups(self):
        """List all available backup files with timestamps

        Returns:
            list: List of tuples (timestamp, filepath) sorted by most recent first
        """
        backup_dir = os.path.dirname(self.NN_FILE_PATH)
        backup_prefix = os.path.basename(self.NN_FILE_PATH) + ".backup."

        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith(backup_prefix):
                backup_path = os.path.join(backup_dir, filename)
                timestamp = filename.replace(backup_prefix, "")
                backups.append((timestamp, backup_path))

        # Sort by timestamp (newest first)
        backups.sort(reverse=True)
        return backups

    def _load(self):
        """Load the neural network from file"""
        if not self._use_file:
            return

        with open(self.NN_FILE_PATH) as nnFile:
            nn = json.load(nnFile)
        self.theta1 = [np.array(li) for li in nn["theta1"]]
        self.theta2 = [np.array(li) for li in nn["theta2"]]
        self.input_layer_bias = [np.array(li) for li in nn["b1"]]
        self.hidden_layer_bias = [np.array(li) for li in nn["b2"]]
