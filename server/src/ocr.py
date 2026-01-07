import numpy as np
import math
import json
import os


class OCRNeuralNetwork:
    NN_FILE_PATH = 'ocr_neural_network.json'
    LEARNING_RATE = 0.1

    def __init__(self, num_hidden_nodes, data_matrix, data_labels, training_indices, use_file=True):
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
        return 1 / (1 + math.e ** -z)

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
            data = {
                'y0': data_matrix[data_index],
                'label': data_labels[data_index]
            }
            
            # Forward propagation
            y1 = np.dot(np.asmatrix(self.theta1), np.asmatrix(data['y0']).T)
            sum1 = y1 + np.asmatrix(self.input_layer_bias)
            y1 = self.sigmoid(sum1)

            y2 = np.dot(np.asmatrix(self.theta2), y1)
            y2 = np.add(y2, np.asmatrix(self.hidden_layer_bias))
            y2 = self.sigmoid(y2)

            # Backpropagation
            actual_vals = [0] * 10
            actual_vals[data['label']] = 1
            output_errors = np.asmatrix(actual_vals).T - np.asmatrix(y2)
            hidden_errors = np.multiply(
                np.dot(np.asmatrix(self.theta2).T, output_errors),
                self.sigmoid_prime(sum1)
            )

            # Update weights
            self.theta1 += (
                self.LEARNING_RATE *
                np.dot(np.asmatrix(hidden_errors), np.asmatrix(data['y0']))
            )
            self.theta2 += (
                self.LEARNING_RATE *
                np.dot(np.asmatrix(output_errors), np.asmatrix(y1).T)
            )
            self.hidden_layer_bias += self.LEARNING_RATE * output_errors
            self.input_layer_bias += self.LEARNING_RATE * hidden_errors

    def train(self, training_data_array):
        """Train the network with new data"""
        for data in training_data_array:
            # Forward propagation
            y1 = np.dot(np.asmatrix(self.theta1), np.asmatrix(data['y0']).T)
            sum1 = y1 + np.asmatrix(self.input_layer_bias)
            y1 = self.sigmoid(sum1)

            y2 = np.dot(np.asmatrix(self.theta2), y1)
            y2 = np.add(y2, np.asmatrix(self.hidden_layer_bias))
            y2 = self.sigmoid(y2)

            # Backpropagation
            actual_vals = [0] * 10
            actual_vals[data['label']] = 1
            output_errors = np.asmatrix(actual_vals).T - np.asmatrix(y2)
            hidden_errors = np.multiply(
                np.dot(np.asmatrix(self.theta2).T, output_errors),
                self.sigmoid_prime(sum1)
            )

            # Update weights
            self.theta1 += (
                self.LEARNING_RATE *
                np.dot(np.asmatrix(hidden_errors), np.asmatrix(data['y0']))
            )
            self.theta2 += (
                self.LEARNING_RATE *
                np.dot(np.asmatrix(output_errors), np.asmatrix(y1).T)
            )
            self.hidden_layer_bias += self.LEARNING_RATE * output_errors
            self.input_layer_bias += self.LEARNING_RATE * hidden_errors

    def predict(self, test):
        """Predict the digit from input data"""
        y1 = np.dot(np.asmatrix(self.theta1), np.asmatrix(test).T)
        y1 = y1 + np.asmatrix(self.input_layer_bias)
        y1 = self.sigmoid(y1)

        y2 = np.dot(np.array(self.theta2), y1)
        y2 = np.add(y2, self.hidden_layer_bias)
        y2 = self.sigmoid(y2)

        results = y2.T.tolist()[0]
        return results.index(max(results))

    def save(self):
        """Save the neural network to file"""
        if not self._use_file:
            return

        json_neural_network = {
            "theta1": [w.tolist() if isinstance(w, np.ndarray) else w
                       for w in self.theta1],
            "theta2": [w.tolist() if isinstance(w, np.ndarray) else w
                       for w in self.theta2],
            "b1": [w.tolist() if isinstance(w, np.ndarray) else w
                   for w in self.input_layer_bias],
            "b2": [w.tolist() if isinstance(w, np.ndarray) else w
                   for w in self.hidden_layer_bias]
        }
        with open(OCRNeuralNetwork.NN_FILE_PATH, 'w') as nnFile:
            json.dump(json_neural_network, nnFile)

    def _load(self):
        """Load the neural network from file"""
        if not self._use_file:
            return

        with open(OCRNeuralNetwork.NN_FILE_PATH) as nnFile:
            nn = json.load(nnFile)
        self.theta1 = [np.array(li) for li in nn['theta1']]
        self.theta2 = [np.array(li) for li in nn['theta2']]
        self.input_layer_bias = [np.array(li) for li in nn['b1']]
        self.hidden_layer_bias = [np.array(li) for li in nn['b2']]

