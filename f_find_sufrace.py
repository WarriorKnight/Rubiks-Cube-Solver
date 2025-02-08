import cv2
import numpy as np
import pickle


def find_area(path):
    # Load your image
    data_to_save = []
    image = cv2.imread(path)
    #cv2.rectangle(image,(450,0),(1000,500),(0,0,0),-1)
    cv2.imshow("Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tresh_val = 200
    # Threshold the image to segment the white regions
    _, thresh = cv2.threshold(gray, tresh_val, tresh_val, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to keep track of the largest contour and its area
    largest_contour = None
    largest_area = 0

    # Iterate through the contours
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    cv2.imshow("Result", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # If a largest contour is found, approximate its shape with a polygon
    if largest_contour is not None:
        epsilon = 0.04 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        if len(approx) == 4:
            # Draw the contour on the original image
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

            # Extract and print the coordinates of the four corners
            for point in approx:
                x, y = point[0]
                data_to_save.append([x, y])
                print(f"Corner: ({x}, {y})") #RT LT BR BL

            # Display the result

            # open a file, where you ant to store the data
            file = open('corner_position', 'wb')

            # dump information to that file
            pickle.dump(data_to_save, file)

            # close the file
            file.close()

            
            cv2.imshow("Result", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return image
        else:
            print("The largest white region does not have 4 corners.")
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

            # Extract and print the coordinates of the four corners
            for point in approx:
                x, y = point[0]
                data_to_save.append([x, y])
                print(f"Corner: ({x}, {y})") #RT LT BR BL
            cv2.imshow("Result", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("No white regions found in the image.")


#find_area('images/ws.png')