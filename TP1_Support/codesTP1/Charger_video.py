#
# Afficher une video à partir d'un fichier local
#
import cv2

capture = cv2.VideoCapture(0)

success, img = capture.read()
while success:
    #Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Video", gray)
    # taper la touche ESC pour arrèter la boucle
    if cv2.waitKey(10) & 0xFF == 27:
        break
    success, img = capture.read()

capture.release()
cv2.destroyWindow("Video")
