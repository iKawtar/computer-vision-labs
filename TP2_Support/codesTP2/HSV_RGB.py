import cv2

img = cv2.imread('ressources/image1.jpg')

b, g, r = cv2.split(img)

cv2.imshow("Rouge", r)
cv2.waitKey(0)
cv2.imshow("Vert", g)
cv2.waitKey(0)
cv2.imshow("Bleu", b)
cv2.waitKey(0)

cv2.imshow("Image couleur", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image niveaux de gris", gray)
cv2.waitKey(0)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s , v = cv2.split(hsv)

cv2.imshow("Hue", h)
cv2.waitKey(0)
cv2.imshow("Saturation", s)
cv2.waitKey(0)
cv2.imshow("Value", v)
cv2.waitKey(0)
cv2.imshow("Image HSV", hsv)
cv2.waitKey(0)

cv2.destroyAllWindows()