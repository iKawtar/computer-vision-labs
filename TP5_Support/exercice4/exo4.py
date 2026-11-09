import cv2
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt

original = cv2.imread("sunflower.png")

gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

noisy = gray.copy()

prob = 0.05

random = np.random.rand(*image.shape[:2])

noisy[random < prob / 2] = 0  # pepper
noisy[random > 1 - prob / 2] = 255  # salt


mean = cv2.blur(gray, (5,5))
gaussian = cv2.GaussianBlur(gray, (5,5), 0)
median = cv2.medianBlur(gray, 5)
bilateral = cv2.bilateralFilter(gray, 9, 75, 75)


def mse(img1, img2):
    return np.mean((img1.astype(float) - img2.astype(float)) ** 2)

print("MSE moyenneur :", mse(gray, mean))
print("MSE gaussien :", mse(gray, gaussian))
print("MSE médian :", mse(gray, median))
print("MSE bilatéral :", mse(gray, bilateral))

plt.figure(figsize=(12, 8))

images = [original, noisy, median, gaussian, mean, bilateral]
titles = ["Originale", "Bruitée", "Median", "Gaussian", "Mean", "Bilateral"]

for i in range(5):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis("off") 

plt.tight_layout()
plt.show()