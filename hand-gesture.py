import cv2
import numpy as np
import math
import pyautogui
import time
import pygetwindow as gw

# Parameters
cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.8  # start point/total height
threshold = 60  # BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0
isBgCaptured = 0  # bool, whether the background captured
triggerSwitch = False  # If true, keyboard simulator works

# Variables for smooth scrolling
prev_y = None  # Previous y position of finger center (to calculate movement)
scroll_sensitivity = 10  # Sensitivity of movement for scrolling
scroll_buffer = []  # Buffer to store the last few positions of the finger center

# Setup camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)

# Initialize background subtraction model
bgModel = None


# Function to remove background
def removeBG(frame):
    fgmask = bgModel.apply(frame, learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


# Function to track finger movement and scrolling
def trackFingerMovement(res, drawing):
    global prev_y, scroll_sensitivity, scroll_buffer

    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                # Get the finger tip position
                finger_tip = far
                cv2.circle(drawing, finger_tip, 8, [211, 84, 0], -1)

                # Track movement
                if prev_y is not None:
                    movement = finger_tip[1] - prev_y
                    scroll_buffer.append(movement)

                # Store the last few movements
                if len(scroll_buffer) > 10:  # Keep last 10 movements for smoothing
                    scroll_buffer.pop(0)

                # If there is enough movement, scroll
                if len(scroll_buffer) > 2:
                    avg_move = sum(scroll_buffer) / len(scroll_buffer)
                    if abs(avg_move) > scroll_sensitivity:
                        if avg_move > 0:
                            pyautogui.scroll(-10)  # Scroll down
                            print("Scrolling Down")
                        elif avg_move < 0:
                            pyautogui.scroll(10)  # Scroll up
                            print("Scrolling Up")

                # Update previous y position
                prev_y = finger_tip[1]
            return True
    return False


# Main loop
while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                  (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    cv2.imshow('original', frame)

    # Perform background subtraction if background is captured
    if isBgCaptured == 1:
        img = removeBG(frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
              int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the region of interest
        cv2.imshow('mask', img)

        # Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('thresh', thresh)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            max_area = -1
            max_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour

            # Find convex hull and defects
            res = max_contour
            hull = cv2.convexHull(res)
            drawing = np.zeros(img.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            trackFingerMovement(res, drawing)

        cv2.imshow('output', drawing)

    # Handle keyboard input
    k = cv2.waitKey(10)
    if k == 27:  # Press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('b'):  # Press 'b' to capture background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1
        print('!!!Background Captured!!!')
    elif k == ord('r'):  # Press 'r' to reset background
        bgModel = None
        isBgCaptured = 0
        print('!!!Reset Background!!!')
