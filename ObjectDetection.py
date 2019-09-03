import cv2
import numpy as np


def nothing():
    pass


vs = cv2.VideoCapture("batsman_facing_video.mp4")

cv2.namedWindow("Trackbar")
cv2.createTrackbar("L-H", "Trackbar", 14, 180, nothing)
cv2.createTrackbar("L-S", "Trackbar", 91, 255, nothing)
cv2.createTrackbar("L-V", "Trackbar", 124, 255, nothing)
cv2.createTrackbar("U-H", "Trackbar", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbar", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbar", 255, 255, nothing)

""" 
 Lower Values
 0, 120, 180
 14, 91, 124
"""

iterator = 0


def save_this_frame_as_image(current_frame, operation_status):
    if operation_status:
        global iterator
        cv2.imwrite('SavedFrames/frame' + str(iterator) + '.jpg', current_frame)

        current_image = cv2.imread('SavedFrames/frame' + str(iterator) + '.jpg')
        current_image = cv2.resize(current_image, (340, 480))
        for x in range(0, 340, 1):
            for y in range(0, 480, 1):
                color = current_image[y, x]
                print(color)

        # extracted_color = int(current_image[300, 300])
        # print(extracted_color)

        iterator += 1

        # if image type is b g r, then b g r value will be displayed.
        # if image is gray then color intensity will be displayed.


while True:

    _, frame = vs.read()

    if frame is None:
        break

    save_this_frame_as_image(frame, True)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbar")
    l_s = cv2.getTrackbarPos("L-S", "Trackbar")
    l_v = cv2.getTrackbarPos("L-V", "Trackbar")

    u_h = cv2.getTrackbarPos("U-H", "Trackbar")
    u_s = cv2.getTrackbarPos("U-S", "Trackbar")
    u_v = cv2.getTrackbarPos("U-V", "Trackbar")

    lower_yellow = np.array([l_h, l_s, l_v])
    upper_yellow = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = np.ones((8, 8), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        modifiedCnt = np.array(cnt).reshape((-1, 1, 2)).astype(np.int32)
        cv2.drawContours(frame, [modifiedCnt], 0, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)  # for correct viewing 50

    if key == ord("q"):
        break

vs.release()
cv2.destroyAllWindows()

""" def print_all_rgb_values_of_frames():
    global iterator
    images = []
    for i in iterator:
        images[i].create(480, 640, CV_8UC3) """
