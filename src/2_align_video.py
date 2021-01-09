import os
import sys
from PySide6 import QtGui, QtWidgets
from math import *


directory =  os.fsencode(sys.argv[1])

filenames = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if not filename.endswith( ('.txt') ): # whatever file types you're using...
        filenames.append(filename)

filenames.sort()

for file in filenames:
    file_txt = sys.argv[1] + "/" + file + ".txt"
    if not os.path.exists(file_txt):
        continue

    # read points
    f = open(file_txt, "r")
    if f == None:
        continue

    l1_x = int(f.readline())
    l1_y = int(f.readline())
    l2_x = int(f.readline())
    l2_y = int(f.readline())

    print(file +" " + str(l1_x)+ ", "+str(l1_y) + " "+ str(l2_x)+ ", "+str(l2_y))
    f.close()

    # calculate angle
    angle = degrees( atan((l2_y-l1_y)/(l2_x-l1_x)) )
    print(angle)

    # rotate
    transform = QtGui.QTransform().rotate(-angle)

    app = QtWidgets.QApplication([])
    picture = QtGui.QPixmap(file)
    picture = picture.transformed(transform)
    picture.save("output.jpg")

    exit()