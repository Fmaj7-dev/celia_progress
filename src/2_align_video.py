import os
import sys
from PySide6 import QtGui, QtWidgets, QtCore
from math import *
import numpy as np


directory =  os.fsencode(sys.argv[1])

filenames = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith( ('.txt') ): # whatever file types you're using...
        filenames.append(filename)

filenames.sort()

i = 0
app = QtWidgets.QApplication([])

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
        print("1st")
        angle = degrees( atan((y1-y2)/(x2-x1)) )
    # second quadrant
    elif x1 > x2 and y1 > y2:
        print("2nd")
        angle = degrees( atan(abs(x1-x2)/abs(y1-y2)) ) +90
    # fourth quadrant
    elif x2 > x1 and y2 > y1:
        print("4th")
        angle = -degrees( atan(abs(y1-y2)/abs(x2-x1)) )
    print("angle: " + str(angle))

    # calculate scale
    xdiff = x1-x2
    ydiff = y1-y2
    distance = sqrt(xdiff*xdiff + ydiff*ydiff)
    multiplier = 400/distance
    print("scale: "+str(multiplier))

    # load pixmap
    pixmap = QtGui.QPixmap(sys.argv[1] + "/" + file)
    width = pixmap.width()
    height = pixmap.height()

    # put it on a bigger pixmap
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
    #scale
    pixmap = pixmap.transformed(scale)
    pixmap.save("output/sans_transformation_"+file, "JPG")
    #translate
    #pixmap = pixmap.transformed(translation2)
    
    
    image = pixmap.toImage()
    image = image.copy(x1-1300,y1-1500,x1+1700,y1+1500)
    pixmap.convertFromImage(image)
    pixmap.save("output/"+file, "JPG")

    print("")

    i += 1
    if i == 10:
        exit()