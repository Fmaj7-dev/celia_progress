import cv2
import numpy as np
import glob
import os
import sys
 
def createVideo(path_to_images, video_name):
    
    #size=(3000, 3000)
    #size=(4032, 3024)
    img_array = []

    # add filenames sorted
    filenames = []
    for file in glob.glob(path_to_images+'*.jpg'):
        filename = os.fsdecode(file)
        filenames.append(filename)

    filenames.sort()  
    print(str(len(filenames))+" jpg files")

    # size of the first image will be the size of the video
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)

    # output video
    out = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    # append to array
    for filename in filenames:
        img = cv2.imread(filename)
        out.write(img)
        print("processing "+filename)
    
    out.release()

if __name__ == "__main__":
    createVideo( sys.argv[1], sys.argv[2] )
