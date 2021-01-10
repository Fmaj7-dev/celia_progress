import os
import sys
from PySide6 import QtGui, QtWidgets
from math import *
import numpy as np


directory =  os.fsencode(sys.argv[1])

filenames = []

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

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

    print("... processing "+ file +" " + str(x1)+ ", "+str(y1) + " "+ str(x2)+ ", "+str(y2))
    f.close()

    angle = 0
    # calculate angle
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
    print("")
    #anglee = degrees(angle_between((1, 0), (l2_x-l1_x, l2_y-l1_y)))
    #print(anglee)

    # rotate
    transform = QtGui.QTransform().rotate(angle)

    picture = QtGui.QPixmap(sys.argv[1] + "/" + file)
    picture = picture.transformed(transform)
    a = picture.save("output_"+file, "JPG")


    i += 1
    if i == 10:
        exit()