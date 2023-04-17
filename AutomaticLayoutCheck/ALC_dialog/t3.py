import cv2
import numpy as np

# Load the two site_components to be compared
img1 = cv2.imread('1.png')
img2 = cv2.imread('3.png')

img1 = cv2.resize(img1, (500, 500))
img2 = cv2.resize(img2, (500, 500))

# Convert the site_components to grayscale
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Compute the Mean Squared Error (MSE) between the two site_components
mse = np.mean((img1_gray - img2_gray)**2)

# Print the MSE value
print("The MSE value between the two site_components is:", mse)

# Код с среднеквадратичной ошибкой
# 257 / 5 000
# Результаты перевода
# Перевод
# Конечно! Другим методом сравнения двух изображений является индекс структурного подобия (SSIM),
# который сравнивает структурное сходство изображений, а не просто сравнивает значения пикселей, как метод MSE.
# Среднеквадратическая ошибка (MSE) — это метод сравнения сходства между двумя изображениями. Это метод сравнения на основе пикселей, который вычисляет среднее значение квадратов различий между соответствующими значениями пикселей в двух изображениях.
#
# MSE рассчитывается путем вычитания значений пикселей двух изображений в каждой соответствующей позиции, затем возведения результата в квадрат и получения среднего значения всех квадратов различий. Чем ниже значение MSE, тем более похожи изображения.

