# Afficher la webcam comme video
import cv2

capture = cv2.VideoCapture(0)                   # lire a partir de la camera par defaut

# configurer les propriétées de la video
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)      # la largeur
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)     # la hauteur
capture.set(cv2.CAP_PROP_BRIGHTNESS, 180)       # la brillance
capture.set(cv2.CAP_PROP_CONTRAST, 50)          # le contraste

success, img = capture.read()
while success:
    cv2.imshow("Webcam", img)
    # Taper sur la touche ESC pour stopper la boucle
    if cv2.waitKey(10) & 0xFF == 27:
        break
    success, img = capture.read()

capture.release()
cv2.destroyWindow("Webcam")