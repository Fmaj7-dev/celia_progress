import os
import sys
import cv2 as cv

# show num_static_frames frames of the same image without changing
num_static_frames = 5
# then show num_blending_frames of the blending image
num_blending_frames = 5
# image sequence number
sequence = 0

# save image with sequence name
def saveNewImage( image ):
    global sequence

    filename = "output2/output_"+str(sequence).zfill(5)+".jpg"
    print("\tsaving "+filename)
    cv.imwrite(filename, image)
    sequence += 1

# iterate through output directory
def processFiles( input ):
    global num_blending_frames
    global num_static_frames

    # get all filenames from directory
    directory =  os.fsencode( input )

    filenames = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith( ('.jpg') ):
            filenames.append(filename)

    filenames.sort()

    for index, name in enumerate(filenames):
        # load image 1
        img1 = cv.imread(input+name)
        #cv.imshow('image', img1)

        for i in range(num_static_frames):
            print( "not blending " + name )
            saveNewImage(img1)
        
        diff = 1/(num_blending_frames+1)
        if (index+1 < len(filenames)):
            # load image 2
            img2 = cv.imread(input+filenames[index+1])

            for i in range(num_blending_frames):
                factor = (i+1)*diff
                print( "blending "+str( factor )+ " "+ name + " and " + filenames[index+1])
                result = cv.addWeighted(img1, 1-factor, img2, factor, 0)
                saveNewImage(result)

if __name__ == "__main__":
    processFiles( sys.argv[1] )
