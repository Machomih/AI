import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Pasul 1: Citirea și pregătirea datelor
data = pd.read_csv('seeds_dataset.txt', sep="\t", header=None)
features = data.iloc[:, :-1].values
labels = data.iloc[:, -1].values - 1

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

train_features, test_features, train_labels, test_labels = train_test_split(scaled_features, labels, test_size=0.2,
                                                                            random_state=42)

# Pasul 2: Inițializarea rețelei
num_features = features.shape[1]
num_hidden_neurons = 10
num_output_classes = len(np.unique(labels))
learning_rate = 0.01
num_epochs = 1000

weights_input_hidden = np.random.randn(num_features, num_hidden_neurons)
bias_hidden = np.zeros((1, num_hidden_neurons))
weights_hidden_output = np.random.randn(num_hidden_neurons, num_output_classes)
bias_output = np.zeros((1, num_output_classes))


# Pasul 3: Definirea funcțiilor de activare și eroare
def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return x > 0


def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=1, keepdims=True)


def cross_entropy_loss(predicted, actual):
    samples = actual.shape[0]
    loss = -np.sum(actual * np.log(predicted)) / samples
    return loss


# Pasul 4: Propagarea înainte
def forward_pass(inputs, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output):
    hidden_layer_input = np.dot(inputs, weights_input_hidden) + bias_hidden
    hidden_layer_output = relu(hidden_layer_input)
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + bias_output
    predicted_output = softmax(output_layer_input)
    return hidden_layer_output, predicted_output


# Pasul 5: Propagarea înapoi
def backward_pass(inputs, actual_labels, hidden_layer_output, predicted_output, weights_hidden_output):
    samples = inputs.shape[0]
    error_output_layer = predicted_output - actual_labels
    grad_weights_hidden_output = np.dot(hidden_layer_output.T, error_output_layer) / samples
    grad_bias_output = np.sum(error_output_layer, axis=0, keepdims=True) / samples
    error_hidden_layer = np.dot(error_output_layer, weights_hidden_output.T)
    error_hidden_layer[hidden_layer_output <= 0] = 0  # Aplicăm derivata ReLU
    grad_weights_input_hidden = np.dot(inputs.T, error_hidden_layer) / samples
    grad_bias_hidden = np.sum(error_hidden_layer, axis=0, keepdims=True) / samples
    return grad_weights_input_hidden, grad_bias_hidden, grad_weights_hidden_output, grad_bias_output


def update_parameters(weights_input_hidden, bias_hidden, weights_hidden_output, bias_output, grad_weights_input_hidden,
                      grad_bias_hidden, grad_weights_hidden_output, grad_bias_output, learning_rate):
    weights_input_hidden -= learning_rate * grad_weights_input_hidden
    bias_hidden -= learning_rate * grad_bias_hidden
    weights_hidden_output -= learning_rate * grad_weights_hidden_output
    bias_output -= learning_rate * grad_bias_output
    return weights_input_hidden, bias_hidden, weights_hidden_output, bias_output


def to_one_hot(labels, num_classes):
    one_hot_labels = np.zeros((labels.size, num_classes))
    one_hot_labels[np.arange(labels.size), labels] = 1
    return one_hot_labels


# Pasul 6: Antrenarea rețelei
def train_network(train_features, train_labels, num_features, num_hidden_neurons, num_output_classes, learning_rate,
                  num_epochs):
    weights_input_hidden = np.random.randn(num_features, num_hidden_neurons)
    bias_hidden = np.zeros((1, num_hidden_neurons))
    weights_hidden_output = np.random.randn(num_hidden_neurons, num_output_classes)
    bias_output = np.zeros((1, num_output_classes))

    train_labels_one_hot = to_one_hot(train_labels, num_output_classes)

    for epoch in range(num_epochs):
        hidden_output, predicted_output = forward_pass(train_features, weights_input_hidden, bias_hidden,
                                                       weights_hidden_output, bias_output)
        loss = cross_entropy_loss(predicted_output, train_labels_one_hot)
        grad_weights_input_hidden, grad_bias_hidden, grad_weights_hidden_output, grad_bias_output = backward_pass(
            train_features, train_labels_one_hot, hidden_output, predicted_output, weights_hidden_output)
        weights_input_hidden, bias_hidden, weights_hidden_output, bias_output = (
            update_parameters(weights_input_hidden,
                              bias_hidden,
                              weights_hidden_output,
                              bias_output,
                              grad_weights_input_hidden,
                              grad_bias_hidden,
                              grad_weights_hidden_output,
                              grad_bias_output,
                              learning_rate))

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss}")

    return weights_input_hidden, bias_hidden, weights_hidden_output, bias_output


# Pasul 7: Testarea rețelei
def predict(test_features, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output):
    _, predicted_output = forward_pass(test_features, weights_input_hidden, bias_hidden, weights_hidden_output,
                                       bias_output)
    predicted_labels = np.argmax(predicted_output, axis=1)
    return predicted_labels


def evaluate_network(test_features, test_labels, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output):
    predicted_labels = predict(test_features, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output)
    accuracy = np.mean(predicted_labels == test_labels)
    return accuracy


# Antrenarea și evaluarea rețelei
trained_weights_input_hidden, trained_bias_hidden, trained_weights_hidden_output, trained_bias_output = train_network(
    train_features, train_labels, num_features, num_hidden_neurons, num_output_classes, learning_rate, num_epochs)
test_accuracy = evaluate_network(test_features, test_labels, trained_weights_input_hidden, trained_bias_hidden,
                                 trained_weights_hidden_output, trained_bias_output)
print(f"Test Accuracy: {test_accuracy}")
