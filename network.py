import numpy as np
import matplotlib.pyplot as plt


def to_one_hot(y, k):
    one_hot = np.zeros(k)
    one_hot[y] = 1
    return one_hot


class Layer:
    def __init__(self, size, input_size, weights=None, biases=None):
        self.size = size
        self.input_size = input_size
        if str(type(weights)) == str(type(None)):
            self.weights = np.random.randn(size, input_size) * 2
        else:
            self.weights = weights
        if str(type(biases)) == str(type(None)):
            self.biases = np.random.randn(size) * 2
        else:
            self.biases = biases

    def forward(self, data):
        aggregation = self.aggregation(data)
        activation = self.activation(aggregation)
        return activation

    def aggregation(self, data):
        return np.dot(self.weights, data) + self.biases

    def activation(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def copy(self):
        return Layer(self.size, self.input_size, self.weights.copy(), self.biases.copy())

    def mutate(self, evol_std, mutate_prob):
        # Same as 'child' but in place
        for k, w in enumerate(self.weights):
            for i in range(len(w)):
                if np.random.rand() < mutate_prob:
                    self.weights[k, i] = np.random.randn() * 2
                else:
                    self.weights[k, i] += evol_std * np.random.randn()
        for k, b in enumerate(self.biases):
            if np.random.rand() < mutate_prob:
                self.biases[k] = np.random.randn()
            else:
                self.biases[k] += evol_std * np.random.randn()


class Network:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.layers = []

    def add_layer(self, size):
        if len(self.layers) > 0:
            input_dim = self.layers[-1].size
        else:
            input_dim = self.input_dim
        self.layers.append(Layer(size, input_dim))

    def feedforward(self, input_data):
        activation = input_data
        for layer in self.layers:
            activation = layer.forward(activation)
        return activation

    def mutate(self, evol_std, mutate_prob):
        for layer in self.layers:
            layer.mutate(evol_std, mutate_prob)

    def copy(self):
        new_nw = Network(self.input_dim)
        for layer in self.layers:
            new_nw.layers.append(layer.copy())
        return new_nw


if __name__ == '__main__':
    my_nw = Network(2)
    my_nw.add_layer(16)
    my_other_nw = my_nw.copy()
    my_other_nw.mutate(0.1, 1e-3)
    print(my_nw.layers[0].weights)
    print(my_other_nw.layers[0].weights)
