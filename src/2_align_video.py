import os
import sys
import cv2
from math import *
import numpy as np


# get all filenames from directory
directory =  os.fsencode(sys.argv[1])

filenames = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith( ('.txt') ):
        filenames.append(filename)

filenames.sort()

#filenames = ["20201212.jpg"]

for file in filenames:
    file_txt = sys.argv[1] + "/" + file + ".txt"
    if not os.path.exists(file_txt):
        continue

    # read points
    f = open(file_txt, "r")
    if f == None:
        continue

    x1 = int(f.readline())
    y1 = int(f.readline())
    x2 = int(f.readline())
    y2 = int(f.readline())

    print("-----> processing "+ file +" " + str(x1)+ ", "+str(y1) + " "+ str(x2)+ ", "+str(y2))
    f.close()

    # calculate angle
    angle = 0
    # first quadrant
    if x2 > x1 and y1 > y2:
        angle = degrees( atan((y1-y2)/(x2-x1)) )
    # second quadrant
    elif x1 > x2 and y1 > y2:
        angle = degrees( atan(abs(x1-x2)/abs(y1-y2)) ) +90
    # fourth quadrant
    elif x2 > x1 and y2 > y1:
        angle = -degrees( atan(abs(y1-y2)/abs(x2-x1)) )
    print("angle: " + str(angle))

    # calculate scale
    xdiff = x1-x2
    ydiff = y1-y2
    distance = sqrt(xdiff*xdiff + ydiff*ydiff)
    multiplier = 400/distance
    print("scale: "+str(multiplier))

    # read image
    img = cv2.imread(sys.argv[1] + "/" + file, cv2.IMREAD_COLOR)
    height, width, channels = img.shape

    #put it on a bigger image
    big_img = np.zeros((6000,6000,3), np.uint8)
    
    x_offset = 1000
    y_offset = 1000
    big_img[y_offset : y_offset + img.shape[0], x_offset : x_offset + img.shape[1]] = img
    img = big_img
    height, width, channels = img.shape
    x1 += 1000
    x2 += 1000
    y1 += 1000
    y2 += 1000

    # rotate
    M = cv2.getRotationMatrix2D((x1, y1), -angle, 1)
    img = cv2.warpAffine(img,M,(width,height))
    #cv2.imwrite("output/cv2_rotation_"+file, img)

    # scale
    img = cv2.resize(img, None, fx=multiplier, fy=multiplier, interpolation = cv2.INTER_CUBIC)
    #cv2.imwrite("output/cv2_scale_"+file, img)

    img_height, img_width, img_channels = img.shape
    print("img_height after scale: " + str(img_height))
    print("img_width after scale: " + str(img_width))
    #height = img_height
    #width = img_width

    x1 = int(multiplier*x1)
    y1 = int(multiplier*y1)
    
    # translate
    #x_offset = 1300-x1
    #y_offset = 1500-y1
    #M = np.float32([[1, 0, x_offset],[0, 1, y_offset]])
    #img = cv2.warpAffine(img,M,(width, height))

    # crop
    img = img[y1-1300:y1+1700, x1-1300:x1+1700]
    #cv2.imwrite("output/cv2_"+file, img)

    #img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(sys.argv[1]+"/cv2_"+file, img)

    print("")
