import os
import sys
#from PySide6 import QtGui, QtWidgets, QtCore
import cv2
from math import *
import numpy as np


directory =  os.fsencode(sys.argv[1])

filenames = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith( ('.txt') ): # whatever file types you're using...
        filenames.append(filename)

filenames.sort()

#filenames = ["20201212.jpg"]
i = 0
#app = QtWidgets.QApplication([])

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
    print(" ### Correction needed")
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
    cv2.imwrite("output/cv2_scale_"+file, img)

    img_height, img_width, img_channels = img.shape
    print("img_height after scale: " + str(img_height))
    print("img_width after scale: " + str(img_width))
    #height = img_height
    #width = img_width

    x1 = int(multiplier*x1)
    y1 = int(multiplier*y1)
    
    # translate
    x_offset = 1300-x1
    y_offset = 1500-y1
    M = np.float32([[1, 0, x_offset],[0, 1, y_offset]])
    img = cv2.warpAffine(img,M,(width, height))

    # crop
    img = img[1000:4000, 1000:4000]
    #cv2.imwrite("output/cv2_crop_"+file, img)
    cv2.imwrite("output/cv2_"+file, img)

    # write output
    

    # load pixmap
    """pixmap = QtGui.QPixmap(sys.argv[1] + "/" + file)

    # put it on a bigger pixmap
    width = pixmap.width()
    height = pixmap.height()

    base = QtGui.QPixmap(10000, 10000)
    painter = QtGui.QPainter()
    painter.begin(base)
    painter.fillRect(QtCore.QRect(0,0,10000, 10000), QtGui.QColor(255, 255, 255))
    offset = 2000
    painter.drawPixmap(offset, offset, offset+width, offset+height, pixmap, 0, 0, width, height)
    painter.end()
    pixmap = base

    x1 += offset
    y1 += offset

    # perform transformations
    mapped = QtCore.QPoint(x1, y1)
    print("before mapping: " + str(mapped))
    
    rotation = QtGui.QTransform().rotate(angle)
    mapped = rotation.map(mapped)
    print("after rotation: " + str(mapped))

    scale = QtGui.QTransform().scale(multiplier, multiplier)
    mapped = scale.map(mapped)
    print("after scale: " + str(mapped))

    translation2 = QtGui.QTransform().translate(1300-mapped.x(), 1500-mapped.y())
    mapped = translation2.map(mapped)
    print("after translation: "+str(mapped))

    # apply transformations
    
    #rotate
    pixmap = pixmap.transformed(rotation)
    pixmap.save("output/after_rotation_"+file, "JPG")
    #scale
    pixmap = pixmap.transformed(scale)
    pixmap.save("output/after_scale_"+file, "JPG")
    
    #translate
    #pixmap = pixmap.transformed(translation2)
    
    
    image = pixmap.toImage()
    image = image.copy(x1-1300,y1-1500,x1+1700,y1+1500)
    pixmap.convertFromImage(image)
    pixmap.save("output/"+file, "JPG")
"""
    print("")

    i += 1
    if i == 10:
        pass#exit()