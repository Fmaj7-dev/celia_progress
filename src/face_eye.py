import numpy as np
import cv2
import sys

face_cascade = cv2.CascadeClassifier("/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")

#eye_cascade = cv2.CascadeClassifier("/anaconda3/lib/python3.7/site-packages/cv2/data/haarcascade_righteye_2splits.xml")

print("processing "+sys.argv[1])
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

height, width = img.shape[:2]

# calculate min and max sizes for opencv search
min_face_size = int(width/4)
max_face_size = int(width*0.9)

faces = face_cascade.detectMultiScale(gray, 1.03, 5, 1, (min_face_size, min_face_size), (max_face_size,max_face_size))
found = False
for (x,y,w,h) in faces:
    found = True
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
     
    cv2.line(img, (x + int(w/2) -10, y + int(h/2)), (x + int(w/2) +10, y + int(h/2)),(255,0,0),2)
    cv2.line(img, (x + int(w/2), y + int(h/2) -10), (x + int(w/2), y + int(h/2) +10),(255,0,0),2)

    # eye min max dimensions
    min_eye_size = int(w/4)
    max_eye_size = int(w/3)

    eyes = eye_cascade.detectMultiScale(roi_gray, 1.03, 5, 1, (min_eye_size, min_eye_size), (max_eye_size,max_eye_size))
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

# rescale for showing it
if not found:
    print("face not found")
    

img_crop = img[y:y+w, x:x+w]
img = img_crop

desired_celia_width = 800
scale_factor = w / desired_celia_width
output_width = int(img.shape[1] / scale_factor)
output_height = int(img.shape[0] / scale_factor)
dim = (output_width, output_height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

cv2.imwrite('output_'+sys.argv[1], resized) 

# show it
#cv2.imshow("img", resized)
#cv2.waitKey(0)
#cv2.destroyAllWindows()