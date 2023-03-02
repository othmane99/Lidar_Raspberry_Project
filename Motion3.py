import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set the resolution of the camera
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize the background subtraction model
bg_subtractor = cv2.createBackgroundSubtractorMOG()

# Initialize the ROI rectangle
roi_rect = None
drawing_roi = False

def draw_roi(event, x, y, flags, param):
    global roi_rect, drawing_roi

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_roi = True
        roi_rect = [x, y, 0, 0]

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing_roi:
            roi_rect[2] = x - roi_rect[0]
            roi_rect[3] = y - roi_rect[1]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing_roi = False
        roi_rect[2] = x - roi_rect[0]
        roi_rect[3] = y - roi_rect[1]

cv2.namedWindow("Motion detection")
cv2.setMouseCallback("Motion detection", draw_roi)

while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Apply the background subtraction model to the frame
    fg_mask = bg_subtractor.apply(frame)

    # Extract the ROI from the frame
    if roi_rect is not None:
        roi_x, roi_y, roi_w, roi_h = roi_rect
        roi = fg_mask[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Apply thresholding to the ROI to create a binary image
        _, binary_roi = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY)

        # Calculate the number of white pixels in the binary ROI
        white_pixel_count = cv2.countNonZero(binary_roi)

        # If the number of white pixels exceeds a threshold, motion is detected
        if white_pixel_count > 100:
            print("Motion detected")

        # Display the ROI rectangle on the frame
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Motion detection", frame)

    # Check if the "r" key is pressed to reset the ROI rectangle
    if cv2.waitKey(1) & 0xFF == ord('r'):
        roi_rect = None

    # Check if the "q" key is pressed to quit the program
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
