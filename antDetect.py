import cv2
import numpy as np
from scipy import signal
from scipy import misc
from scipy.signal import argrelextrema

cap = cv2.VideoCapture('fullAnts.mp4')

import cv2
import numpy as np;

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200


# Filter by Area.
params.filterByArea = True
params.minArea = 10

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.1

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

meas=[]
pred=[]
mp = np.array((2,1), np.float32) # measurement

while(cap.isOpened()):

    ret, frame = cap.read()
    frame2 = frame
    cv2.imshow('original', frame)
    

    keypoints = detector.detect(frame)
    for keyPoint in keypoints:
        x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
        y = int(keyPoint.pt[1])
        print x
        print y
        frame2[x,y] = [255,255,0]

        mp = np.array([[np.float32(x)],[np.float32(y)]])
        meas.append((x,y))


    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show blobs
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.imshow('tracks', frame2)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
