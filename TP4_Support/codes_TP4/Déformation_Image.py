import cv2
import numpy as np
import fonctions.Traitement_Image as ti

import fonctions.dessin as ds

dessin = False
couleur_final = (0, 255, 0)
couleur_dessin = (0, 0, 255)
largeur, hauteur= 320,480
points = []


def perspective_warp(image, points, width, height):
    source = np.float32(points)
    destination = np.float32([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1],
    ])
    matrix = cv2.getPerspectiveTransform(source, destination)
    return cv2.warpPerspective(image, matrix, (width, height))


def on_mouse(event, x, y, flags, param):
    global points, dessin, img, img_bk, tiroc, warped_image
    if event == cv2.EVENT_LBUTTONDOWN:
        dessin = True
        add_point(points, (x, y))
        if len(points) == 4:
            dess_polygone(img, points, (x, y), True)
            dessin = False
            img_bk = tiroc.image.copy()
            warped_image = perspective_warp(tiroc.image, points, largeur, hauteur)
            points.clear()
            cv2.imshow("Perspective Warping", warped_image)
    elif event == cv2.EVENT_MOUSEMOVE:
        if dessin == True:
            img = img_bk.copy()
            dess_polygone(img, points, (x, y))

def add_point(points, curt_pt):
    print("Adding point #%d with position(%d,%d)"
          % (len(points), curt_pt[0], curt_pt[1]))
    points.append(curt_pt)

def dess_polygone(img, points, curt_pt, is_final=False):
    if (len(points) > 0):
        if is_final == False:
            ds.dess_polylignes(img, np.array([points]), False, couleur_final)
            ds.dess_ligne(img, points[-1], curt_pt, couleur_dessin)
        else:
            ds.dess_polylignes(img, np.array([points]), True, couleur_final)
        for point in points:
            ds.dess_cercle(img, point, 2, couleur_final, 2)
            ds.dess_text(img, str(point), point, 0.5, couleur_final)

def print_instruction(img):
    txtInstruction = "Left click to specify four points to warp image. ESC to exit, 's' to save"
    ds.dess_text(img,txtInstruction, (10, 20), 0.5, (255, 255, 255))
    print(txtInstruction)


if __name__ == "__main__":
    global img, img_bk, tiroc, warped_image

    title = "Original Image"
    tiroc = ti.TraitementImage(title, 'ressources/book_perspect1.jpg')  
    img = tiroc.image
    img_bk = img.copy()
    print_instruction(img)
    cv2.imshow(title, img)
    cv2.setMouseCallback(title, on_mouse)

    while True:
        cv2.imshow(title, img)
        ch = cv2.waitKey(10)
        if (ch & 0xFF) == 27:
            break
        elif ch == ord('s'):
            filepath = 'ressources/book_sauv.jpg'
            cv2.imwrite(filepath, warped_image)
            print("File saved to " + filepath)
    cv2.destroyAllWindows()

