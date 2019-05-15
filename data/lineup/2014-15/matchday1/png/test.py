import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('2014316_lu-Juventus.png', 0)
img = cv2.medianBlur(img, 5)

cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=20,param2=40,minRadius=0,maxRadius=16)
print "detected %s circles" % (len(circles))
circles = np.uint16(np.around(circles))
row, col = img.shape
print "row: %s, col: %s" % (row, col)
for index, i in enumerate(circles[0,:]):

    if i[0] <= row and i[1] <= col:
        print "i[2] = %s" % i[2]
        px = img[i[0]-2, i[1]]
        if px == 255 and i[2] < 17:
            print "drawing circle %s" % index
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            print "px is: %s" % px
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
