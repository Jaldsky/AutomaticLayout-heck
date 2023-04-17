# Чтобы сравнить два изображения с помощью машинного обучения, вы можете использовать предварительно обученную модель сходства изображений. Одной из таких моделей является сиамская нейронная сеть, представляющая собой архитектуру нейронной сети, специально разработанную для сравнения двух изображений.


import tensorflow as tf
import cv2

# Load the pre-trained Siamese Neural Network model
model = tf.keras.models.load_model('siamese_model.h5')

# Load the two site_components to be compared
img1 = cv2.imread('1.png')
img2 = cv2.imread('3.png')

# Resize the site_components to the same size as expected by the model
img1 = cv2.resize(img1, (224, 224))
img2 = cv2.resize(img2, (224, 224))

# Convert the site_components to float32 data type and normalize the pixel values
img1 = tf.image.convert_image_dtype(img1, tf.float32)
img2 = tf.image.convert_image_dtype(img2, tf.float32)
img1 = tf.keras.applications.mobilenet_v2.preprocess_input(img1)
img2 = tf.keras.applications.mobilenet_v2.preprocess_input(img2)

# Create a batch of size 2 with the two site_components
batch = tf.stack([img1, img2], axis=0)

# Use the model to predict the similarity score between the two site_components
similarity_score = model.predict(batch)[0][0]

# Print the similarity score
print("The similarity score between the two site_components is:", similarity_score)








