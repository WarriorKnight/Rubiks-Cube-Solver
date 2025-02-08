import matplotlib
import PIL
import cv2

img = PIL.Image.open('images/wss.png')
converter = PIL.ImageEnhance.Color(img)
img2 = converter.enhance(0.5)
cv2.imshow('Original Image', img2)
cv2.imshow('Increased Saturation', img)
cv2.waitKey(0)
cv2.destroyAllWindows()