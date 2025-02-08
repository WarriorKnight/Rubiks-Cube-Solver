import cv2
import numpy as np

# Load an image
image = cv2.imread('images/12.png')

# Convert the image from BGR to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Increase the saturation (modify the second parameter for different levels of saturation)
saturation_factor = 20.0  # Increase saturation by a factor of 2
hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)

# Convert the image back to BGR color space
result_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

# Display the original and modified images
cv2.imshow('Original Image', image)
cv2.imshow('Increased Saturation', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the modified image
cv2.imwrite('increased_saturation_image.jpg', result_image)