import numpy as np
import tensorflow as tf
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Lambda
from keras.models import Model
from keras import backend as K

# Define input shape
input_shape = (128, 128, 3)

# Define the base network architecture
def build_base_network(input_shape):
    input_layer = Input(shape=input_shape)
    x = Conv2D(32, kernel_size=(3, 3), activation='relu')(input_layer)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(256, kernel_size=(3, 3), activation='relu')(x)
    x = Flatten()(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    return Model(input_layer, x)

# Define the Siamese Network architecture
def build_siamese_network(base_network, input_shape):
    input_a = Input(shape=input_shape)
    input_b = Input(shape=input_shape)
    processed_a = base_network(input_a)
    processed_b = base_network(input_b)
    distance = Lambda(lambda x: K.sqrt(K.sum(K.square(x[0]-x[1]), axis=1, keepdims=True)))([processed_a, processed_b])
    model = Model([input_a, input_b], distance)
    return model

# Load test data
test_data = np.load('test_data.npy')

# Define number of pairs to test
num_pairs = test_data.shape[0]

# Define labels for test pairs (0 if images are the same, 1 if images are different)
test_labels = np.zeros((num_pairs, 1))
test_labels[num_pairs//2:] = 1

# Load the pre-trained base network weights
base_network = build_base_network(input_shape)
base_network.load_weights('base_network_weights.h5')

# Build the Siamese Network
siamese_network = build_siamese_network(base_network, input_shape)

# Compile the Siamese Network
siamese_network.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Evaluate the Siamese Network on test data
test_loss, test_accuracy = siamese_network.evaluate([test_data[:,0], test_data[:,1]], test_labels)

print(f'Test loss: {test_loss:.4f} - Test accuracy: {test_accuracy:.4f}')