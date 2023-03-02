
import cv2
import numpy as np
from static_roi import staticROI

# Create an instance of the staticROI class
static_roi = staticROI()

# Call the update (updateRE) method to start capturing and displaying frames
static_roi.update()

# After the user selects and crops an ROI, display the cropped image
static_roi.show_cropped_ROI()

# Wait for the user to press a key
cv2.waitKey(0)

# Destroy all windows and release the video capture object
cv2.destroyAllWindows()
static_roi.capture.release()
