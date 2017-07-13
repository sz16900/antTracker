import numpy as np
import cv2

cv2.namedWindow("tracking")
camera = cv2.VideoCapture("/home/seth/openCV_Tests/Exploring_openCV/cut.mp4")
bbox = (638.0,230.0,56.0,101.0)
tracker = cv2.Tracker_create("KCF")
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



while camera.isOpened():
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
        ok = tracker.init(image, bbox)
        init_once = True

    ok, newbox = tracker.update(image)
    print ok, newbox

    if ok:
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))

    cv2.imshow("tracking", image)
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break # esc pressed