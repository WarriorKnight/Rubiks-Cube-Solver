import cv2
import numpy as np
import pickle

def perspective_transform(image):

    file = open('corner_position', 'rb')

    # dump information to that file
    data = pickle.load(file)

    # close the file
    file.close()

    temp_src_points = []
    for item in data:
        temp_src_points.append(item)
    #print(temp_src_points)

    side = 600
    # Load the image

    # Define the four points of the region to be transformed
    src_points = np.array([temp_src_points[1], temp_src_points[0], temp_src_points[3],temp_src_points[2]], dtype=np.float32)

    # Define the corresponding points in the output (desired) image
    dst_points = np.array([[0, 0], [side, 0], [side, side], [0, side]], dtype=np.float32)

    # Compute the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transform
    transformed_image = cv2.warpPerspective(image, matrix, (side, side))

    # Crop the transformed region
    x, y, w, h = 0, 0, side, side
    cropped_image = transformed_image[y:y + h, x:x + w]
    return cropped_image
    # Save the transformed and cropped image
    #cv2.imwrite('output_image.jpg', cropped_image)

    # Display the original and transformed images
    #cv2.imshow('Transformed and Cropped Image', cropped_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
