import cv2
import numpy as np
import glob
import os
 
size=(3000, 3000)
img_array = []

# add filenames sorted
filenames = []
for file in glob.glob('output/*.jpg'):
    filename = os.fsdecode(file)
    filenames.append(filename)

filenames.sort()    

# append to array
for filename in filenames:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

 
 # output video
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 4, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()