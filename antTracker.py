# Implementing tracker to make sure bouynding box are not lost or switched
# by accident.
# Should I run the simpleBlobDetection every so often? 10 frames. per frame?
# this will ensure that new ants are tracked

import numpy as np
import cv2

camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
mask = cv2.imread('mask.png')
tracker = cv2.MultiTracker("KCF")
file = open("tracks.txt","w+")
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

#  Bounding box parameters
length = 14
width = 10
frame = 0

#  Start from frame 350 to avoid the third ant walking by
camera.set(1,frame)

##################################################################################################

def vectorize(A, B):
	return (B[0]-A[0],B[1]-A[1])

##################################################################################################

while camera.isOpened():
    ok, image = camera.read()
    frame = frame + 1
    #places the mask on the top left corner
    image[y_offset:y_offset+mask.shape[0], x_offset:x_offset+mask.shape[1]] = mask
    keypoints = detector.detect(image)
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

###################################################################################################  
# This is to write in file.... seems a bit too much to do this loop twice. 
    cnt = 0
    for newbox in boxes:
        cnt = cnt + 1
        # Left top most point
        A = (int(newbox[0]), int(newbox[1]))
        # Write to file
        file.write("%d %d %d %d\r\n" % (frame, cnt, A[0]+7, A[1]+7))

##################################################################################################

# SO, FOR NOW, i CAN DETECT THAT AN ANT IS OUTSIDE OF ITS BOUNDING BOX, I RESET THE THING AND MOVE ON
# NOW i NEED TO FIGURE OUT A WAY TO KEEP THEIR IDS


	# https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
	# https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
    for keyPoint in keypoints:
        x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
        y = int(keyPoint.pt[1])
        M = [x,y]
        # mp = np.array([[np.float32(x)],[np.float32(y)]])
        # meas.append((x,y))
        # Is this point inside any of the squares??
        outside = 0
        # inside = 0
        print len(keypoints)
        for newbox in boxes:
            # Left top most point
            A = (int(newbox[0]), int(newbox[1]))
            # Right top most point
            B = (int(newbox[0] + 15), int(newbox[1]))
            # Right bottom most point
            C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            # Draw rectangle image
            cv2.rectangle(image, A, C, (200,100,0))
            if (0 <= np.dot(vectorize(A,B), vectorize(A,M)) <= np.dot(vectorize(A,B), vectorize(A,B))) and \
               (0 <= np.dot(vectorize(B,C), vectorize(B,M)) <= np.dot(vectorize(B,C), vectorize(B,C))):
    			print True
            else:
    			print False
    			outside = outside + 1
                # keypoints = detector.detect(image)
                # im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # cv2.rectangle(image, A, C, (200,100,0))
        # This is to say that if there are more or less thatn 2 ants, then skip .... just checking        
        if len(keypoints) != 2:
            print "Next"
            # Thhis numbers are magic, they need to be dynamic
        else:
            if outside == 2:
                # while True:
                #     key2 = cv2.waitKey(1) or 0xff
                #     cv2.imshow("tracking", image)
                #     if key2 == ord('p'):
                #         break
                # I need to somehow restart the tracker
                # keypoints = detector.detect(image)
                # if detector fails
                # I need to find a way to keep the ones that are ok and only reset the one that I lost.
                if len(keypoints) == 0:
                    bbox = (0, 0, 15, 15)
                    tracker = cv2.MultiTracker("KCF")
                    ok = tracker.add(image, bbox)
                    file.write("RESET\r\n")

                else:
                    if len(keypoints) > 1:
                        x = int(keypoints[0].pt[0] - 5) #i is the index of the blob you want to get the position
                        y = int(keypoints[0].pt[1] - 5)
                        bbox1 = (x, y, 15,15)
                        x1 = int(keypoints[1].pt[0] - 5) #i is the index of the blob you want to get the position
                        y1 = int(keypoints[1].pt[1] - 5)
                        bbox2 = (x1, y1, 15,15)
                        tracker = cv2.MultiTracker("KCF")
                        ok = tracker.add(image, (bbox1,bbox2))
                        file.write("RESET\r\n")
                    else :
                        x = int(keypoints[0].pt[0] - 5) #i is the index of the blob you want to get the position
                        y = int(keypoints[0].pt[1] - 5)
                        bbox1 = (x, y, 15,15)
                        tracker = cv2.MultiTracker("KCF")
                        ok = tracker.add(image, bbox1)
                        file.write("RESET\r\n")


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