from keras.datasets import mnist
import numpy as np

# Load MNIST dataset
(x_train, y_train), _ = mnist.load_data()

# Normalize pixel values to be between 0 and 1
x_train = x_train.astype('float32') / 255

# Define number of pairs to create
num_pairs = 100000

# Initialize arrays to store pairs and labels
pairs = np.zeros((num_pairs, 2, 28, 28))
labels = np.zeros((num_pairs,))

# Define indices for each digit class
digit_indices = [np.where(y_train == i)[0] for i in range(10)]

# Create pairs of site_components and their corresponding labels
for i in range(num_pairs):
    # Choose a random digit class
    digit_class = np.random.randint(0, 10)

    # Choose two random site_components from the chosen digit class
    image_indices = np.random.choice(digit_indices[digit_class], size=2, replace=False)
    pair = x_train[image_indices]
    pairs[i] = pair

    # Assign label of 1 if site_components are from the same digit class, 0 otherwise
    if i % 2 == 0:
        labels[i] = 1
    else:
        labels[i] = 0

# Reshape pairs to have shape (num_pairs, 2, 28, 28, 1) for input to a Convolutional Neural Network
train_data = pairs.reshape(num_pairs, 2, 28, 28, 1)

train_labels = labels.astype('int32')






from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Lambda
from keras.models import Model, load_model
import keras.backend as K

# Define input shape
input_shape = (224, 224, 3)

# Define base network
input_image = Input(shape=input_shape)
x = Conv2D(32, (3, 3), activation='relu')(input_image)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(256, (3, 3), activation='relu')(x)
x = Flatten()(x)
x = Dense(512, activation='relu')(x)
base_network = Model(input_image, x)

# Define inputs
input_a = Input(shape=input_shape)
input_b = Input(shape=input_shape)

# Process inputs with base network
processed_a = base_network(input_a)
processed_b = base_network(input_b)

# Define distance function
def euclidean_distance(vectors):
    x, y = vectors
    sum_squared = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_squared, K.epsilon()))

# Define distance layer
distance_layer = Lambda(euclidean_distance)([processed_a, processed_b])

# Define final model
model = Model(inputs=[input_a, input_b], outputs=distance_layer)

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
model.fit([train_data[:, 0], train_data[:, 1]], train_labels, batch_size=64, epochs=10)

# Save model
model.save('siamese_model.h5')

# # Load model
# loaded_model = load_model('path/to/siamese_model.h5')
#
# # Evaluate model
# score = loaded_model.evaluate([test_data[:, 0], test_data[:, 1]], test_labels, verbose=0)
#
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])