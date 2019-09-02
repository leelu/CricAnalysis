import cv2
import numpy as np
import time
from imutils.video import VideoStream

cap = cv2.VideoCapture("batsman_facing_video.mp4")

time.sleep(2.0)

while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    yellowLower = (23, 41, 133)
    yellowUpper = (40, 150, 255)
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        ctr = np.array(contour).reshape((-1, 1, 2)).astype(np.int32)
        cv2.drawContours(frame, [ctr], 0, (0, 255, 0), 1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(50)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
