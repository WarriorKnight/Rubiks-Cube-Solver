import cv2
import numpy as np
import pickle

x1, y1 = 0, 0
x2, y2 = 0,0
margin = 30
calibration = False
list_of_colors =        [[0,0,60],          #WHITE
                         [0,0,50],          #RED
                         [0,0,40],           #BLUE
                         [0,0,30],          #ORANGE
                         [0,0,20],           #GREEN
                         [0,0,10]]          #YELLOW
list_of_colors_names =  ["WHITE",
                         "RED",
                         "BLUE",
                         "GREEN",
                         "ORANGE",
                         "YELLOW"]

def average_rgb(colors):
    colors = np.array(colors)
    avg_color = np.mean(colors, axis=0, dtype=int)
    return avg_color.tolist()

def closest(colors,color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    #print(index_of_smallest[0][0])
    return index_of_smallest[0] 

def ScanAllColors(path):
    image = cv2.imread(path)
    width = image.shape[1]
    height = image.shape[0]
    actual_colors = []

    file = open('color_calibration', 'rb')
    data = pickle.load(file)
    file.close()  


    for x,item in enumerate(data):
         list_of_colors[x] = item

    print(list_of_colors)

             

    i = 0
    for y in range(3):
        for x in range(3):         
            i = i + 1
            x1, y1 = int(width/3)*x + margin, int(height/3)*y + margin
            x2, y2 = int(width/3)*x + int(width/3)-margin,int(height/3)*y + int(height/3)-margin
            roi = image[y1:y2, x1:x2]
            print(x1,y1)
            average_color = np.mean(roi, axis=(0, 1))   
            average_color = average_color.astype(int)
            average_color_rgb = average_color[::-1]
            average_color_rgb = average_color_rgb.tolist()

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (x1, y1)
            fontScale = 0.5

            if calibration:
                #closest_color = closest(list_of_colors,average_color_rgb)
                #print(closest_color)
                image = cv2.putText(image, str(average_color_rgb), org, font,  #list_of_colors_names[int(closest_color)]
                           fontScale, (0, 0, 0) , 1, cv2.LINE_AA) 
                actual_colors.append(average_color_rgb)
            else:
                closest_color = closest(list_of_colors,average_color_rgb)
                print(average_color_rgb)
                print(list_of_colors_names[closest_color[0]])
                image = cv2.putText(image, str(average_color_rgb), org, font,  #list_of_colors_names[int(closest_color)]
                           fontScale, (0, 0, 0) , 1, cv2.LINE_AA) 
                actual_colors.append(closest_color)
            
    #cv2.imshow('Image with ROI', image)
    #cv2.waitKey(0)
    print(" ")
    if calibration:
        return actual_colors
    else:
        return actual_colors
         
print(ScanAllColors("images/calibration/101.png"))

if calibration:
    white_val = 0
    blue_val = 0
    green_val = 0
    red_val = 0
    orange_val = 0
    yellow_val = 0

    returned = ScanAllColors('images/calibration/0.png')
    white_val = average_rgb(returned)

    returned = ScanAllColors('images/calibration/1.png')
    del returned[3]
    del returned[4-1]
    del returned[5-2]
    red_val = average_rgb(returned)

    returned = ScanAllColors('images/calibration/2.png')
    del returned[1]
    del returned[4-1]
    del returned[7-2]
    blue_val = average_rgb(returned)

    returned = ScanAllColors('images/calibration/3.png')
    del returned[3]
    del returned[4-1]
    del returned[5-2]
    orange_val = average_rgb(returned)

    returned = ScanAllColors('images/calibration/4.png')
    del returned[1]
    del returned[4-1]
    del returned[7-2]
    green_val = average_rgb(returned)
    
    returned = ScanAllColors('images/calibration/5.png')
    del returned[2]
    del returned[4-1]
    del returned[8-2]
    yellow_val = average_rgb(returned)

    list_of_colors[0] = white_val
    list_of_colors[1] = red_val
    list_of_colors[2] = blue_val
    list_of_colors[3] = green_val
    list_of_colors[4] = orange_val
    list_of_colors[5] = yellow_val
    calibration = False


    file = open('color_calibration', 'wb')
    # dump information to that file
    pickle.dump(list_of_colors, file)
    # close the file
    file.close()
    print("Calibration completed")

#ScanAllColors('images/test.jpg')
#print(actual_colors)


#cv2.imshow('ROI', roi)
#cv2.imshow('Image with ROI', image)
cv2.waitKey(0)
cv2.destroyAllWindows()