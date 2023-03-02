import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set the resolution of the camera
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the region of interest (ROI)
roi_x = 200
roi_y = 100
roi_width = 200
roi_height = 200

# Initialize the background subtraction model
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Apply the background subtraction model to the frame
    fg_mask = bg_subtractor.apply(frame)

    # Extract the ROI from the frame
    roi = fg_mask[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # Apply thresholding to the ROI to create a binary image
    _, binary_roi = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY)

    # Calculate the number of white pixels in the binary ROI
    white_pixel_count = cv2.countNonZero(binary_roi)

    # If the number of white pixels exceeds a threshold, motion is detected
    if white_pixel_count > 100:
        print("Motion detected")

    # Display the frame with the ROI
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 255, 0), 2)
    cv2.imshow("Motion detection", frame)

    # Exit the loop if the "q" key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
