# Implementing tracker to make sure bouynding box are not lost or switched
# by accident.
# Should I run the simpleBlobDetection every so often? 10 frames. per frame?
# this will ensure that new ants are tracked

import numpy as np
import cv2

camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
tracker = cv2.MultiTracker("KCF")
init_once = False
meas=[]
mp = np.array((2,1), np.float32) # measurement

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

#  Start from frame 350 to avoid the third ant walking by
camera.set(1,350)

#  Bounding box parameters
length = 15
width = 10
frame = 5

##################################################################################################

def vectorize(A, B):
	return (B[0]-A[0],B[1]-A[1])

##################################################################################################

while camera.isOpened():
    ok, image = camera.read()
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

 ##################################################################################################
    
    for keyPoint in keypoints:
	    x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
	    y = int(keyPoint.pt[1])
	    M = [x,y]
	    mp = np.array([[np.float32(x)],[np.float32(y)]])
	    # meas.append((x,y))
	    # Is this point inside any of the squares??
	    outside = 0

##################################################################################################

	    for newbox in boxes:

	    	# Left top most point
	        A = (int(newbox[0]), int(newbox[1]))
	    	# Right top most point
	        B = (int(newbox[0] + 15), int(newbox[1]))
	    	# Right bottom most point
	        C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
	        # Draw rectangle image
	        cv2.rectangle(image, A, C, (200,100,0))
			# https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
			# https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not
	        if (0 <= np.dot(vectorize(A,B), vectorize(A,M)) <= np.dot(vectorize(A,B), vectorize(A,B))) and \
	           (0 <= np.dot(vectorize(B,C), vectorize(B,M)) <= np.dot(vectorize(B,C), vectorize(B,C))):
    			print True
	        else:
    			print False
    			outside = outside + 1
    			if outside == len(boxes):
    				# I need to somehow restart the tracker
    				while True:
						key2 = cv2.waitKey(1) or 0xff
						cv2.imshow("Keypoints", im_with_keypoints)
						if key2 == ord('p'):
							break

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
    frame = frame + 1
    print "Frame: ", frame
    print "\n"
##################################################################################################

cap.release()
cv2.destroyAllWindows()