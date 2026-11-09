import cv2
import numpy as np


FILTERS = ["Original", "Median", "Gaussian", "Mean", "Bilateral", "Sobel", "Laplacian", "Canny"]
selected_filter_index = 0


def odd_kernel(value):
    """Convertit un curseur en taille de noyau impaire."""
    return 2 * value + 1


def nothing(_value):
    pass


def choose_filter(event, x, y, _flags, _param):
    global selected_filter_index

    if event != cv2.EVENT_LBUTTONDOWN or not 10 <= y <= 55:
        return

    button_width = 150
    index = x // button_width
    if 0 <= index < len(FILTERS):
        selected_filter_index = index


def show_filter_buttons():
    button_width = 150
    panel = 255 * np.ones((75, button_width * len(FILTERS), 3), dtype="uint8")

    for index, filter_name in enumerate(FILTERS):
        left = index * button_width
        right = left + button_width - 5
        color = (60, 170, 60) if index == selected_filter_index else (210, 210, 210)
        cv2.rectangle(panel, (left, 10), (right, 55), color, -1)
        cv2.rectangle(panel, (left, 10), (right, 55), (80, 80, 80), 1)
        text_size = cv2.getTextSize(filter_name, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)[0]
        text_x = left + (button_width - text_size[0]) // 2
        cv2.putText(panel, filter_name, (text_x, 39), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 0, 0), 1)

    cv2.imshow("Filtres", panel)


def apply_filter(frame):
    selected_filter = FILTERS[selected_filter_index]

    if selected_filter == "Original":
        return frame, selected_filter

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if selected_filter == "Median":
        kernel = odd_kernel(max(1, cv2.getTrackbarPos("Noyau", "Parametres")))
        return cv2.medianBlur(frame, kernel), f"Median | noyau={kernel}"

    if selected_filter == "Gaussian":
        kernel = odd_kernel(max(1, cv2.getTrackbarPos("Noyau", "Parametres")))
        sigma = cv2.getTrackbarPos("Sigma", "Parametres") / 10
        return cv2.GaussianBlur(frame, (kernel, kernel), sigma), (
            f"Gaussian | noyau={kernel}, sigma={sigma:.1f}"
        )

    if selected_filter == "Mean":
        kernel = odd_kernel(max(1, cv2.getTrackbarPos("Noyau", "Parametres")))
        return cv2.blur(frame, (kernel, kernel)), f"Mean | noyau={kernel}"

    if selected_filter == "Bilateral":
        diameter = max(1, cv2.getTrackbarPos("Diametre", "Parametres"))
        sigma_color = max(1, cv2.getTrackbarPos("Sigma couleur", "Parametres"))
        sigma_space = max(1, cv2.getTrackbarPos("Sigma espace", "Parametres"))
        result = cv2.bilateralFilter(frame, diameter, sigma_color, sigma_space)
        return result, (
            f"Bilateral | d={diameter}, couleur={sigma_color}, espace={sigma_space}"
        )

    if selected_filter == "Sobel":
        direction = cv2.getTrackbarPos("Direction Sobel", "Parametres")
        kernel = odd_kernel(max(1, cv2.getTrackbarPos("Noyau", "Parametres")))
        if direction == 0:
            sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel)
            label = "X"
        elif direction == 1:
            sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel)
            label = "Y"
        else:
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel)
            sobel = cv2.magnitude(sobel_x.astype("float32"), sobel_y.astype("float32"))
            label = "magnitude"
        result = cv2.convertScaleAbs(sobel)
        return result, f"Sobel | direction={label}, noyau={kernel}"

    if selected_filter == "Laplacian":
        kernel = odd_kernel(max(1, cv2.getTrackbarPos("Noyau", "Parametres")))
        result = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel))
        return result, f"Laplacian | noyau={kernel}"

    low = cv2.getTrackbarPos("Seuil bas", "Parametres")
    high = max(low + 1, cv2.getTrackbarPos("Seuil haut", "Parametres"))
    aperture = odd_kernel(max(1, cv2.getTrackbarPos("Aperture Canny", "Parametres")))
    result = cv2.Canny(gray, low, high, apertureSize=aperture)
    return result, f"Canny | bas={low}, haut={high}, aperture={aperture}"


cv2.namedWindow("Filtres")
cv2.setMouseCallback("Filtres", choose_filter)
cv2.namedWindow("Parametres")
cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

cv2.createTrackbar("Noyau", "Parametres", 2, 10, nothing)
cv2.createTrackbar("Sigma", "Parametres", 10, 100, nothing)
cv2.createTrackbar("Diametre", "Parametres", 5, 15, nothing)
cv2.createTrackbar("Sigma couleur", "Parametres", 75, 255, nothing)
cv2.createTrackbar("Sigma espace", "Parametres", 75, 255, nothing)
cv2.createTrackbar("Direction Sobel", "Parametres", 2, 2, nothing)
cv2.createTrackbar("Seuil bas", "Parametres", 50, 255, nothing)
cv2.createTrackbar("Seuil haut", "Parametres", 150, 255, nothing)
cv2.createTrackbar("Aperture Canny", "Parametres", 1, 3, nothing)

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Impossible d'ouvrir la webcam.")

while True:
    success, frame = camera.read()
    if not success:
        print("Impossible de lire une image depuis la webcam.")
        break

    filtered, label = apply_filter(frame)
    show_filter_buttons()
    display = filtered.copy()
    if display.ndim == 2:
        display = cv2.cvtColor(display, cv2.COLOR_GRAY2BGR)
    cv2.putText(display, label, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.imshow("Webcam", display)

    key = cv2.waitKey(1) & 0xFF
    if key in (ord("q"), 27):
        break
    if key == ord("s"):
        cv2.imwrite("capture_filtre.png", filtered)
        print("Image enregistree dans capture_filtre.png")

camera.release()
cv2.destroyAllWindows()