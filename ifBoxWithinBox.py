# Implementing tracker to make sure bounding box are not lost or switched
# by accident.
# Should I run the simpleBlobDetection every so often? 10 frames. per frame?
# this will ensure that new ants are tracked


# TO DO:
    # Tracker now RESETS when two bounding boxes are too close to each other. I need to also check if a box is left behind.
    # This will not work for a Social Carry

import numpy as np
import cv2
from scipy.spatial import distance


camera = cv2.VideoCapture("/home/seth/Host_AntVideos/Examples/edited_video/00001a.mp4")
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



##################################################################################################

def vectorize(A, B):
    return (B[0]-A[0],B[1]-A[1])

##################################################################################################

# This seems to crash my whole computer
videoLength = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
print videoLength 

# Start from frame 350 to avoid the third ant walking by
camera.set(1,frame)

while camera.isOpened():

    ok, image = camera.read()
    frame = frame + 1

    # Stop video two frame before to avoid problems
    if frame > (videoLength - 2):
        print "Here"
        break

    # places the mask on the top left corner
    image[y_offset:y_offset+mask.shape[0], x_offset:x_offset+mask.shape[1]] = mask

    # Detect blobs per frame
    keypoints = detector.detect(image)

    # First initializer
    if opened <= 1:
        for keyPoint in keypoints:
            x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
            y = int(keyPoint.pt[1])
            mp = np.array([[np.float32(x)],[np.float32(y)]])
            meas.append((x,y))
            opened = 2

    if not ok:
        print 'no image read'
        break

    if not init_once:
        # add a list of boxes:
        bbox1 = (meas[0][0] - 5, meas[0][1] - 5, length, length) 
        bbox2 = (meas[1][0] - 5, meas[1][1] - 5, length, length)
        ok = tracker.add(image, (bbox1,bbox2))
        init_once = True

    ok, boxes = tracker.update(image)

    centerPointBox = {}
    cnt = 0
    for newbox in boxes:

        A = (int(newbox[0]), int(newbox[1]))
        C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        centerPointBox[cnt] = [A[0]+7, A[1]+7]

        if cnt == 0:
            cv2.rectangle(image, A, C, (0,0,255))
        if cnt == 1:
            cv2.rectangle(image, A, C, (0,0,0))

# This is to write in file.... seems a bit too much to do this loop twice. 
        file.write("%d %d %d %d\r\n" % (frame, cnt, A[0]+7, A[1]+7)) 
        cnt += 1

##################################################################################################
# This is to check distances.
# This distance is arbitrary. Here I am saying that if two boxes are too close, then reset.
    i = distance.euclidean(centerPointBox[0], centerPointBox[1])
    if i < 4.0 and len(keypoints) == 2: 

        # https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
        # https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not

        centerPointBox = {}

        # For now, I leave this at to just as a reference. I am using two ants anyways.
        if len(keypoints) == len(boxes):

            for keyPoint in keypoints:
                x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
                y = int(keyPoint.pt[1])
                M = [x,y]
                
                outside = 0
                antNum = 0
                cnt = 0

                # Loop the tracking boxes (should be the same number of keypoints)
                for newbox in boxes:

                    antNum += 1

                    # Left top most point
                    A = (int(newbox[0]), int(newbox[1]))
                    # Add the center point of the tracking boxes (the # 7 is because the boxes are length in size)
                    centerPointBox[cnt] = [A[0]+7, A[1]+7]
                    cnt += 1
                    # Right top most point
                    B = (int(newbox[0] + length), int(newbox[1]))
                    # Right bottom most point
                    C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))

                    # Check if the keyPoint is inside any of the boxes
                    if (0 <= np.dot(vectorize(A,B), vectorize(A,M)) <= np.dot(vectorize(A,B), vectorize(A,B))) and \
                       (0 <= np.dot(vectorize(B,C), vectorize(B,M)) <= np.dot(vectorize(B,C), vectorize(B,C))):
                        print True

                    # If it is outside, increment by one. This to make sure that it is trully outside as sometimes the ant could still be
                    # inside its box
                    else:
                        print False
                        outside = outside + 1

                # For some reason, the outside need to match the keypoints. I need to check this further
                if outside == len(keypoints):
                    print "RESET: ", frame
                    file.write("RESET\r\n")

                    keyPointList = {}
                    keyPointListTemp = {}
                    cnt2 = 0
                    for keyPoint2 in keypoints:
                        x = int(keyPoint2.pt[0]) #i is the index of the blob you want to get the position
                        y = int(keyPoint2.pt[1])
                        M = [x,y]
                        keyPointList[cnt2] = M
                        cnt2 += 1

                    print "Box Center: ", centerPointBox
                    print "Keypoints: ", keyPointList

                    for key, value in centerPointBox.iteritems():
                        smallDict = list()
                        for keyAft, valueAft in keyPointList.iteritems():

                            i = distance.euclidean(value, valueAft)
                            smallDict.append(i)

                        # get the index of the min distance. This is based on their position. Needs to be
                        # better as it only assumes. Its quite greedy
                        keyPointListTemp[key] = keyPointList[smallDict.index(min(smallDict))]
                   
                    print "Keypoints Temp: ", keyPointListTemp

                        # if two points are the same, keep it as it was before
                        # FOR NOW, I AM KEEPING JUST FOR THE FIRST ELEMTS. THIS NEES TO BE CHANGED ACCORDINGLY
                        # Perhaps there is a Love Traingle or something similar. Might as well keep it as it is 
                        # and document it
                    if keyPointListTemp[0][0] == keyPointListTemp[1][0]:
                        x = int(keypoints[1].pt[0] - 5) #i is the index of the blob you want to get the position
                        y = int(keypoints[1].pt[1] - 5)
                        bbox2 = (x, y, length,length)
                        x1 = int(keypoints[0].pt[0] - 5) #i is the index of the blob you want to get the position
                        y1 = int(keypoints[0].pt[1] - 5)
                        bbox1 = (x1, y1, length,length)

                        print "NORMAL"
                        # Need to print something out here in the file, because the reset is back to how it was
                            

                    # Else, update the nex boxes
                    else:
                        x = keyPointListTemp[0][0] - 5 #i is the index of the blob you want to get the position
                        y = keyPointListTemp[0][1] - 5
                        bbox1 = (x, y, length,length)
                        x1 = keyPointListTemp[1][0] - 5 #i is the index of the blob you want to get the position
                        y1 = keyPointListTemp[1][1] - 5
                        bbox2 = (x1, y1, length,length)
                        print "The Other"


                    tracker = cv2.MultiTracker(algorithm
                )
                    ok = tracker.add(image, (bbox1,bbox2))
                    ok, boxes = tracker.update(image)

                        



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
cv2.destroyAllWindows()
file.close()