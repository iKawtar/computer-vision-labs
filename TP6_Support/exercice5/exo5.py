import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("synthetic.jpg")


def detect_corners(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    corners = cv2.cornerHarris(
        gray,
        blockSize=2,
        ksize=3,
        k=0.04
    )
    corners = cv2.dilate(corners, None)

    result = input_image.copy()
    result[corners > 0.01 * corners.max()] = [0, 0, 255]
    return result


def rotate_image(input_image, angle):
    height, width = input_image.shape[:2]
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Agrandit la sortie pour ne pas couper les coins après rotation.
    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])
    new_width = int(height * sin + width * cos)
    new_height = int(height * cos + width * sin)
    matrix[0, 2] += (new_width - width) / 2
    matrix[1, 2] += (new_height - height) / 2

    return cv2.warpAffine(input_image, matrix, (new_width, new_height))


images = [
    ("Originale", image),
    ("Rotation de 36 degrés", rotate_image(image, 36)),
    ("Taille 50 %", cv2.resize(image, None, fx=0.5, fy=0.5)),
    ("Taille 150 %", cv2.resize(image, None, fx=1.5, fy=1.5)),
]

plt.figure(figsize=(12, 8))
for number, (title, transformed_image) in enumerate(images, start=1):
    result = detect_corners(transformed_image)
    plt.subplot(2, 2, number)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title(title)

plt.tight_layout()
plt.show()