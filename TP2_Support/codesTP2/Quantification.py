import cv2
import numpy as numpy
img = cv2.imread("ressources/image1.jpg")

height, width, _ = img.shape

for y in range(height):
    for x in range(width):
        blue, green, red = img[y, x]

        # Niveau de gris
        gray = 0.114 * blue + 0.587 * green + 0.299 * red

        # Quantification : 0 à 5
        if gray <= 42:
            level = 0
        elif gray <= 84:
            level = 1
        elif gray <= 126:
            level = 2
        elif gray <= 168:
            level = 3
        elif gray <= 210:
            level = 4
        else:
            level = 5

        # Conversion du niveau 0-5 vers 0-255
        value = level * 51

        img[y, x] = (value, value, value)

cv2.imshow("Image en niveaux de gris", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img=cv2.resize(img,(0,0),fx=1,fy=1.5)
print("valeur pixel =",img[100,100])
img[40:80,40:80]=(0,0,0)
cv2.imshow("affichage",img)
bleu = img.copy()
bleu[:,:,1]=0
bleu[:,:,2]=0
cv2.imshow("bleu",bleu)
rouge = img.copy()
rouge[:,:,0]=0
rouge[:,:,1]=0
cv2.imshow("rouge",rouge)

vert = img.copy()
vert[:,:,0]=0
vert[:,:,2]=0
cv2.imshow("vert",vert)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v=cv2.split(hsv)
cv2.imshow("Hue",h)
cv2.imshow("Saturation",s)
cv2.imshow("Luminosité",v)
cv2.waitKey(0)
cv2.destroyAllWindows()