from f_transform import *
from f_find_sufrace import *
import cv2
import numpy as np


#find white area
#transform images
#extract colors


#PHASE 1, calibrate CUBE FACE AND SAVE
#>>>>>FINDS CUBE FACE, AND SAVES THE COORDINATES
find_area('images/ws.png')


#image2 = perspective_transform(cv2.imread("images/calibration/0.png"))
#cv2.imwrite("images/calibration/0.png", image2)
#
#image2 = perspective_transform(cv2.imread("images/calibration/1.png"))
#cv2.imwrite("images/calibration/1.png", image2)
#
#image2 = perspective_transform(cv2.imread("images/calibration/2.png"))
#cv2.imwrite("images/calibration/2.png", image2)
#
#image2 = perspective_transform(cv2.imread("images/calibration/3.png"))
#cv2.imwrite("images/calibration/3.png", image2)
#
#image2 = perspective_transform(cv2.imread("images/calibration/4.png"))
#cv2.imwrite("images/calibration/4.png", image2)

#image2 = perspective_transform(cv2.imread("images/image.png"))
#cv2.imshow('Image', image2)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

