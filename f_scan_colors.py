import cv2
import numpy as np
import pickle
import f_global
import os
import f_read_write
import f_solver
from f_transform import *
from f_find_sufrace import *


def saturate_image(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Increase the saturation (modify the second parameter for different levels of saturation)
    saturation_factor = 1.4  # Increase saturation by a factor of 2
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
    # Convert the image back to BGR color space
    result_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return result_image

def average_rgb(colors):
    colors = np.array(colors)
    avg_color = np.mean(colors, axis=0, dtype=int)
    return avg_color.tolist()

def closest_rgb(color,colors):
    colors = np.array(colors)
    color = np.array(color)
    #print(color, colors)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    #print(index_of_smallest[0][0])
    return index_of_smallest[0] 

def scan_all_colors(image, skip):
    width = image.shape[1]
    height = image.shape[0]
    actual_colors = []
    x1,y1,x2,y2 = 0,0,0,0
    margin = 40
    i = 0
    for y in range(3):
        for x in range(3):         
            i = i + 1
            if i not in skip:
                x1, y1 = int(width/3)*x + margin, int(height/3)*y + margin
                x2, y2 = int(width/3)*x + int(width/3)-margin,int(height/3)*y + int(height/3)-margin
                roi = image[y1:y2, x1:x2]
                average_color = np.mean(roi, axis=(0, 1))   
                average_color = average_color.astype(int)
                average_color_rgb = average_color[::-1]
                average_color_rgb = average_color_rgb.tolist()
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX 
                fontScale = 0.5
                a_rgb = f_read_write.read("color_calibration")
                image = cv2.putText(image, str(rgb_to_name([average_color_rgb], a_rgb)) + str(i), (x1, y1), font, fontScale, (0, 0, 0) , 1, cv2.LINE_AA) 
                actual_colors.append(average_color_rgb)

    cv2.imwrite("images/comp/1.png", image)
    #cv2.imshow('Image with ROI', image)
    #cv2.waitKey(0)
    return actual_colors

def calibrate_stock_colors():
    average_color_array = []
    for i, filename in enumerate(os.listdir("images/calibration/")):
        f = os.path.join("images/calibration/", filename)
        if os.path.isfile(f):
            average_color = average_rgb(scan_all_colors(saturate_image(perspective_transform(cv2.imread(f))),f_global.calibration_missed_colors[i]))
            average_color_array.append(average_color)
    f_read_write.write("color_calibration", average_color_array)
            
def rgb_to_name(c_rgb,a_rgb):
    colors_list=[]
    for i in c_rgb:
        colors_list.append(f_global.color_names[closest_rgb(i,a_rgb)[0]])
    return colors_list

def invert_index(part_array):
    full_array = [1,2,3,4,5,6,7,8,9]
    for i in part_array:
        full_array.remove(i)
    #print(full_array)
    return full_array

def scan_faces():
    total_scan = 0
    a_rgb = f_read_write.read("color_calibration")
    kokosak = 0
    #for i in range(11):
        #print("--",i)
        #print(len(f_global.scramble_missed_colors[i]) + len(f_global.scramble_indexes[i]))
    
    scramble = ""
    for i in range(11):
        c_rgb = scan_all_colors(saturate_image(perspective_transform(cv2.imread("images/scramble/" + str(i) + ".png"))),f_global.scramble_missed_colors[i])
        inverted_index = invert_index(f_global.scramble_missed_colors[i])
        total_scan = total_scan + len(inverted_index)

        color_list = rgb_to_name(c_rgb,a_rgb)
        #print(f_global.cube_scramble)
        #print(color_list)
        for x, item in enumerate(color_list):
            kokosak += 1
            #print(kokosak, f_global.array_index[kokosak-1], "asdasdasd")
            #print(f_global.color_codes[f_global.color_names.index(item)], (int(f_global.scramble_sides_order[i])-1)*9+inverted_index[x]-1)
            f_global.cube_scramble[f_global.array_index[kokosak-1]-1] = f_global.color_codes[f_global.color_names.index(item)]
            #f_global.cube_scramble[(int(f_global.scramble_sides_order[i])-1)*9+inverted_index[x]-1] = f_global.color_codes[f_global.color_names.index(item)]

            #f_global.cube_scramble[(int(f_global.scramble_sides_order[i])-1)*9 + int(f_global.scramble_indexes[i][x])-1] = f_global.color_codes[f_global.color_names.index(item)]

            #print(f_global.color_codes[f_global.color_names.index(item)], (int(f_global.scramble_sides_order[i])-1)*9+inverted_index[x]-1)
            #f_global.cube_scramble[(int(f_global.scramble_sides_order[i])-1)*9 + f_global.scramble_indexes[i][x]-1] = f_global.color_codes[f_global.color_names.index(item)]
        
    right_order = [1,5,3,2,6,4]
    mixed = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in range(6):
        for x in range(9):
            mixed[(right_order[i]-1)*9+x] = f_global.cube_scramble[(i)*9+x]
    for x in f_global.cube_scramble:
            scramble = scramble + str(x)

    new_scramble = ""
    for x in range(6):
        reversed = scramble[(x)*9:(x+1)*9][::-1]
        new_scramble = new_scramble + str(reversed)
    print(new_scramble)
    print(f_solver.FindSolution(new_scramble), "final")
    



if __name__ == "__main__":
    f_global.init()
    #calibrate_stock_colors()
    scan_faces()
    #print(f_global.array_index[13])

    
