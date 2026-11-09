import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("sunflower.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

noisy = image.copy()

# Add salt and pepper noise
prob = 0.05

random = np.random.rand(*image.shape[:2])

noisy[random < prob / 2] = 0  # pepper
noisy[random > 1 - prob / 2] = 255  # salt

median = cv2.medianBlur(noisy, 5)
gaussian = cv2.GaussianBlur(noisy, (5, 5), 0)
mean = cv2.blur(noisy, (5, 5))

plt.figure(figsize=(12, 8))

images = [image, noisy, median, gaussian, mean]
titles = ["Originale", "Bruitée", "Median", "Gaussian", "Mean"]

for i in range(5):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis("off") 

plt.tight_layout()
plt.show()




