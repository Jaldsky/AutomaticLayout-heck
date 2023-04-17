import cv2

# Load the two site_components to be compared
img1 = cv2.imread('1.png')
img2 = cv2.imread('3.png')

img1 = cv2.resize(img1, (500, 500))
img2 = cv2.resize(img2, (500, 500))

# Convert the site_components to grayscale
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Compute the Mean Structural Similarity Index (MSSIM) between the two site_components
mssim = cv2.matchTemplate(img1_gray, img2_gray, cv2.TM_CCOEFF_NORMED)[0][0]

# Print the MSSIM value
print("The MSSIM value between the two site_components is:", mssim)

# Индекс среднего структурного сходства (MSSIM) — это метод сравнения сходства между двумя изображениями. Он основан на индексе структурного сходства (SSIM), который сравнивает структурное сходство изображений, а не просто сравнивает значения пикселей, как метод среднеквадратичной ошибки (MSE).
#
# MSSIM рассчитывается путем сначала разделения изображений на маленькие окна, а затем вычисления SSIM между соответствующими окнами в двух изображениях. SSIM представляет собой комбинацию трех факторов: яркости, контраста и структуры. Он измеряет, насколько хорошо совпадают яркость, контрастность и структура окон между двумя изображениями.
#
# Когда SSIM вычисляется для всех окон, MSSIM рассчитывается как среднее значение всех значений SSIM. MSSIM находится в диапазоне от 0 до 1, где значение 1 означает, что два изображения идентичны, а значение 0 означает, что они совершенно разные.
#
# Метод MSSIM широко используется в приложениях для обработки изображений, таких как сжатие изображений, восстановление изображений и оценка качества изображений. Это более надежный метод сравнения изображений, чем метод MSE, поскольку он учитывает структурное сходство изображений и меньше подвержен влиянию шума и других искажений.