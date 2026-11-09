import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image_bruitee.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

g3 = cv2.GaussianBlur(image, (3, 3), 0)
g7 = cv2.GaussianBlur(image, (7, 7), 0)
g15 = cv2.GaussianBlur(image, (15, 15), 0)

g310 = cv2.GaussianBlur(image, (3, 3), 10)
g710 = cv2.GaussianBlur(image, (7, 7), 10)
g1510 = cv2.GaussianBlur(image, (15, 15), 10)

g3100 = cv2.GaussianBlur(image, (3, 3), 100)
g7100 = cv2.GaussianBlur(image, (7, 7), 100)
g15100 = cv2.GaussianBlur(image, (15, 15), 100)

plt.figure(figsize=(12, 10))

for i, (img, title) in enumerate([
    (image, "Originale.jpg"),
    (g3, "Gaussian 3x3.jpg"),
    (g7, "Gaussian 7x7.jpg"),
    (g15, "Gaussian 15x15.jpg"),
    (g310, "Gaussian sigma=10 3x3.jpg"),
    (g710, "Gaussian sigma=10 7x7.jpg"),
    (g1510, "Gaussian sigma= 10 15x15.jpg"),
    (g3100, "Gaussian sigma=100 3x3.jpg"),
    (g7100, "Gaussian sigma=100 7x7.jpg"),
    (g15100, "Gaussian sigma= 100 15x15.jpg")
]):

    # L'originale est centrée sur la première ligne, puis chaque sigma occupe une ligne.
    position = 2 if i == 0 else i + 2
    plt.subplot(4, 3, position)
    plt.imshow(img)
    plt.title(title)
    plt.axis("off")
    image_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(title, image_bgr)

plt.show()