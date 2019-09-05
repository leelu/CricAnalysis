from collections import deque
import numpy as np
import cv2
import imutils
import time

# Take in the video
vs = cv2.VideoCapture('batsman_facing_video.mp4')

# Define Color Values
lower_yellow = (14, 91, 125)
upper_yellow = (180, 255, 255)

# initialize the list of tracked points, the frame counter, and the coordinate deltas
pts = deque(maxlen=32)
counter = 0
(dX, dY) = (0, 0)
direction = ""

# allow the camera or video file to warm up
time.sleep(2.0)

while True:

    current_frame = vs.read()

    current_frame = current_frame[1]

    # if we have reached the end of frame
    if current_frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(current_frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "yellow", then perform a series of dilation and erosion to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # only proceed if at least one contour was found
    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(current_frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(current_frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

            # loop over the set of tracked points
            for i in np.arange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    continue

                # check to see if enough points have been accumulated in
                # the buffer
                if counter >= 10 and i == 1 and pts[-10] is not None:
                    thickness = int(np.sqrt(32 / float(i + 1)) * 1.0)
                    cv2.line(current_frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame
        cv2.imshow("Testing Frame", current_frame)
        key = cv2.waitKey(15) & 0xFF
        counter += 1

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

vs.release()
cv2.destroyAllWindows()
