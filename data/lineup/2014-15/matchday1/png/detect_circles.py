import cv2
import numpy as np

img_name = "2014316_lu-Juventus.png"
original = cv2.imread(img_name)
imgray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# retval, image = cv2.threshold(original, 50, 255, cv2.THRESH_BINARY)

# el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# image = cv2.dilate(imgray, el, iterations=6)
#
cv2.imwrite("dilated.png", imgray)

im2, contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)

drawing = cv2.imread(img_name)

centers = []
radii = []
for contour in contours:
    area = cv2.contourArea(contour)

    # there is one contour that contains all others, filter it out
    if area > 500:
        continue

    br = cv2.boundingRect(contour)
    radii.append(br[2])

    m = cv2.moments(contour)
    center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
    centers.append(center)

print("There are {} circles".format(len(centers)))

radius = int(np.average(radii)) + 5

for center in centers:
    cv2.circle(drawing, center, 3, (255, 0, 0), -1)
    cv2.circle(drawing, center, radius, (0, 255, 0), 1)

cv2.imwrite("drawing.png", drawing)
