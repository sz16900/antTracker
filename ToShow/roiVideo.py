# TO DO:
    # Tracker now RESETS when two bounding boxes are too close to each other. I need to also check if a box is left behind.
    # Color code different boxes
    # Also, the boxes should have numbers displayed, to be able to adjust them
    # I think another window which displays the tracks (with a slider bar)
    # I think another window which displays the history of the movement of the bounding box (with a slider bar)
    # Rewind video with slider
    # Need to test whether changing the tracker manually also overwrites the tracks.
    # Start splitting file into different objects OOP oriented

import numpy as np
import cv2
from scipy.spatial import distance
import sys

camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
mask = cv2.imread('mask.png')
algorithm = "KCF"
tracker = cv2.MultiTracker(algorithm)

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

##################################################################################################

def vectorize(A, B):
    return (B[0]-A[0],B[1]-A[1])

##################################################################################################
roi = False
cv2.namedWindow("Keypoints");
cv2.moveWindow("Keypoints", 500,50);

# Save tracks in a dictonary
tracks = {}

# This seems to crash my whole computer
videoLength = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
print videoLength 

# Start from frame 350 to avoid the third ant walking by
camera.set(1,frame)

while camera.isOpened():

    ok, image = camera.read()
    frame = frame + 1
    print "Frame:", frame
    key4 = cv2.waitKey(1)

    # Stop video two frame before to avoid problems
    if frame > (videoLength - 2):
        print "Here"
        break

    # Sets the frame in which to move to
    if key4 == ord('x'):
        # Make sure only valid numbers and no letters are entered
        frame = int(raw_input("Please enter the frame you wish to seek: "))
        boxess = list()
        for newbox in tracks[frame]:
            bbox = (newbox[0], newbox[1], newbox[2], newbox[3])
            boxess.append(bbox)
        tracker = cv2.MultiTracker(algorithm)
        for bboxes in boxess:
            tracker.add(image, bboxes)
        camera.set(1,frame)
        ok, image = camera.read()
        ok, boxes = tracker.update(image)

        # Check that user enters something valid no words, and only within range
        var = raw_input("Please enter the id of the ant to be re-adjusted: ")
        while var != "done":
            var = int(var)
            r = cv2.selectROI(image)
            boxess[var] = (r[0] - 5, r[1] - 5, length, length)
            var = raw_input("Please enter the id of the ant to be re-adjusted: ")
        tracker = cv2.MultiTracker(algorithm)
        for bboxes in boxess:
            tracker.add(image, bboxes)
        ok, boxes = tracker.update(image)

    # Pauses the video
    if key4 == ord('p'):

        while True:
            key2 = cv2.waitKey(1) or 0xff
            cv2.imshow("Keypoints", im_with_keypoints)
            if key2 == ord('p'):
                break

    # Press ESC to quit
    if key4 == 27: 
        break

    # Initialize the video by selecting, manually, the ants to track
    if roi == False:
        boxess = list()
        tracker = cv2.MultiTracker(algorithm)
        r = cv2.selectROI(image)
        bbox = (r[0] - 5, r[1] - 5, length, length)
        boxess.append(bbox)
        while True:
            key2 = cv2.waitKey(1) or 0xff
            if key2 == ord(' '):
                r = cv2.selectROI(image)
                bbox = (r[0] - 5, r[1] - 5, length, length)
                boxess.append(bbox)
            if key2 == ord('q'):
                break
        for bboxes in boxess:
            tracker.add(image, bboxes)
        ok, boxes = tracker.update(image)
        roi = True

    # Changes the bounding box of the ant by id
    if key4 == ord('c'):
        boxess = list()
        for newbox in boxes:
            bbox = (newbox[0], newbox[1], newbox[2], newbox[3])
            boxess.append(bbox)
        # Check that user enters something valid no words, and only within range
        var = raw_input("Please enter the id of the ant to be re-adjusted: ")
        while var != "done":
            var = int(var)
            r = cv2.selectROI(image)
            boxess[var] = (r[0] - 5, r[1] - 5, length, length)
            var = raw_input("Please enter the id of the ant to be re-adjusted: ")
        tracker = cv2.MultiTracker(algorithm)
        for bboxes in boxess:
            tracker.add(image, bboxes)
        ok, boxes = tracker.update(image)

    # places the mask on the top left corner
    image[y_offset:y_offset+mask.shape[0], x_offset:x_offset+mask.shape[1]] = mask

    # Detect blobs per frame
    keypoints = detector.detect(image)
    ok, boxes = tracker.update(image)

    centerPointBox = {}
    cnt = 0
    tracksInFrame = list()

    for newbox in boxes:

        A = (int(newbox[0]), int(newbox[1]))
        C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        centerPointBox[cnt] = [A[0]+7, A[1]+7]

        if cnt == 0:
            cv2.rectangle(image, A, C, (0,0,255))
        if cnt == 1:
            cv2.rectangle(image, A, C, (0,255,0))
        else: 
            cv2.rectangle(image, A, C, (0,0,0))
        
        cnt += 1

        # Save tracks if this frame in list
        tracksInFrame.append(newbox)
    # Store all the tracks in the dictonary based on its frame
    tracks[frame] = tracksInFrame


##################################################################################################
# This is to check distances.
# This distance is arbitrary. Here I am saying that if two boxes are too close, then reset.
    
    # i = distance.euclidean(centerPointBox[0], centerPointBox[1])
    # if i < 3.0 and len(keypoints) == 2: 

    #     roi = False
    

##################################################################################################

    # Show blobs
    im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Keypoints", image)
    if not ok:
        break



##################################################################################################

camera.release()
cv2.destroyAllWindows()

##################################################################################################
# Write to file

file = open("tracks.txt","w+")

# Write the header of the file
file.write("FRAME   ID  X   Y\r\n")

# Bring the frame back to the beginning to be written onto file
frame = 1
for key, value in tracks.iteritems():
    count = 0
    for valu in value:
        file.write("%d %d %d %d\r\n" % (key, count, int(valu[0]), int(valu[1])))
        count += 1


file.close()