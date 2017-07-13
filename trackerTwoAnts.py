import numpy as np
import cv2

cv2.namedWindow("tracking")
camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
bbox = (638.0,230.0,56.0,101.0)
tracker = cv2.MultiTracker("KCF")
init_once = False
meas=[]
mp = np.array((2,1), np.float32) # measurement

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
cnt = 0



while camera.isOpened():
    cnt = cnt + 1
    ok, image=camera.read()
    keypoints = detector.detect(image)
    if opened <= 1:
        for keyPoint in keypoints:
            x = int(keyPoint.pt[0]) #i is the index of the blob you want to get the position
            y = int(keyPoint.pt[1])
            print x
            print y

            mp = np.array([[np.float32(x)],[np.float32(y)]])
            meas.append((x,y))
            opened = 2
    if not ok:
        print 'no image read'
        break

    if not init_once:
        # Minus 5 because the point is in the middle and the 5 because it is half of the square
        bbox = (meas[0][0] - 5, meas[0][1] - 5, 15, 15)
        ok = tracker.add(image, bbox)
        init_once = True

    ok, boxes = tracker.update(image)
    print ok, boxes

    print len(boxes)
    for newbox in boxes:
        # Left top most point
        A = (int(newbox[0]), int(newbox[1]))
        # Right top most point
        B = (int(newbox[0] + 15), int(newbox[1]))
        # Right bottom most point
        C = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        # Draw rectangle image
        cv2.rectangle(image, A, C, (200,100,0))

    cv2.imshow("tracking", image)
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break # esc pressed

    if cnt == 12:
        keypoints = detector.detect(image)
        # if detector fails
        if len(keypoints) == 0:
            bbox = (0, 0, 15, 15)
            tracker = cv2.MultiTracker("KCF")
            ok = tracker.add(image, bbox)
        else:
            x = int(keypoints[0].pt[0] - 5) #i is the index of the blob you want to get the position
            y = int(keypoints[0].pt[1] - 5)
            bbox1 = (x, y, 15,15)
            if len(keypoints) > 1:
                x1 = int(keypoints[1].pt[0] - 5) #i is the index of the blob you want to get the position
                y1 = int(keypoints[1].pt[1] - 5)
                bbox2 = (x1, y1, 15,15)
            tracker = cv2.MultiTracker("KCF")
            ok = tracker.add(image, (bbox1,bbox2))

        cnt = 0
        while True:
            key2 = cv2.waitKey(1) or 0xff
            cv2.imshow("tracking", image)
            if key2 == ord('p'):
                break