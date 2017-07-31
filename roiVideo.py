# Implementing tracker to make sure bounding box are not lost or switched
# by accident.
# Should I run the simpleBlobDetection every so often? 10 frames. per frame?
# this will ensure that new ants are tracked

# TO DO:
    # Tracker now RESETS when two bounding boxes are too close to each other. I need to also check if a box is left behind.

import numpy as np
import cv2
from scipy.spatial import distance
from random import randint


camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
mask = cv2.imread('mask.png')
algorithm = "KCF"
tracker = cv2.MultiTracker(algorithm)
file = open("tracks.txt","w+")

# Write the header of the file
file.write("FRAME   ID  X   Y\r\n")

init_once = False

meas=[]
mp = np.array((2,1), np.float32) # measurement

##################################################################################################
# MASK STUFF 

x_offset=y_offset= 0

##################################################################################################

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
opened = 0

##################################################################################################

# Bounding box parameters
length = 15
width = 10
frame = 0

# Start from frame 350 to avoid the third ant walking by
camera.set(1,frame)


##################################################################################################

def vectorize(A, B):
    return (B[0]-A[0],B[1]-A[1])

##################################################################################################
roi = False
while camera.isOpened():


    ok, image = camera.read()
    frame = frame + 1

    key = cv2.waitKey(1) or 0xff

    if key == ord('p') or roi == False:
        boxess = list()

        print "Inside Roi"
        tracker = cv2.MultiTracker(algorithm)
        r = cv2.selectROI(image)
        print "Roi size: ", r
        bbox = (r[0] - 5, r[1] - 5, length, length)
        boxess.append(bbox)
        # ok = tracker.add(image, bbox)
        while True:
            key2 = cv2.waitKey(1) or 0xff
            if key2 == ord(' '):
                r = cv2.selectROI(image)
                bbox = (r[0] - 5, r[1] - 5, length, length)
                boxess.append(bbox)
                # ok = tracker.add(image, bbox)
            if key2 == ord('q'):
                break
        for bboxes in boxess:
            tracker.add(image, bboxes)
        ok, boxes = tracker.update(image)
        print "Length of boxes: ", boxes
        roi = True



    elif key == ord('c'):
        ok, boxes = tracker.update(image)
        tracker = cv2.MultiTracker(algorithm)
        boxess = list()
        for newbox in boxes:
            print newbox
            boxess.append(newbox)
        while True:
            key3 = cv2.waitKey(1) or 0xff
            if key3 == ord('3'):
                r = cv2.selectROI(image)
                boxess[1] == (r[0] - 5, r[1] - 5, length, length)
                print boxess[1]
                break
        for bboxes in boxess:
            print bboxes
            # tracker.add(image, bboxes)




    else:
        # places the mask on the top left corner
        image[y_offset:y_offset+mask.shape[0], x_offset:x_offset+mask.shape[1]] = mask

        # Detect blobs per frame
        keypoints = detector.detect(image)

        
        ok, boxes = tracker.update(image)

        centerPointBox = {}
        cnt = 0
        for newbox in boxes:

            A = (int(newbox[0]), int(newbox[1]))
            C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            centerPointBox[cnt] = [A[0]+7, A[1]+7]

            # if cnt == 0:
            #     cv2.rectangle(image, A, C, (0,0,255))
            # if cnt == 1:
            #     cv2.rectangle(image, A, C, (0,0,randint(0, 255)))
            cv2.rectangle(image, A, C, (0,0,255))


    # This is to write in file.... seems a bit too much to do this loop twice. 
            file.write("%d %d %d %d\r\n" % (frame, cnt, A[0]+7, A[1]+7)) 
            cnt += 1

    ##################################################################################################
    # This is to check distances.
    # This distance is arbitrary. Here I am saying that if two boxes are too close, then reset.
        
        i = distance.euclidean(centerPointBox[0], centerPointBox[1])
        if i < 3.0 and len(keypoints) == 2: 

            roi = False

    ##################################################################################################

        # Show blobs
        im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        key = cv2.waitKey(1) & 0xff

        if not ok:
            break

        if key == ord('p'):

            while True:
                key2 = cv2.waitKey(1) or 0xff
                cv2.imshow("Keypoints", im_with_keypoints)
                if key2 == ord('p'):
                    break

        cv2.imshow("Keypoints", im_with_keypoints)

        if key == 27: 
            break
##################################################################################################

camera.release()
camera.destroyAllWindows()
file.close()