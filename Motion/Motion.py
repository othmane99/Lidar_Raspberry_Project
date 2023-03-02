import cv2

class MotionDetector(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        self.selected_ROI = False

        self.update()

    def update(self):
        while True:
            if self.capture.isOpened():
                # Read frame
                (self.status, self.frame) = self.capture.read()
                gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                fgmask = self.fgbg.apply(gray_frame)
                cv2.imshow('image', fgmask)
                key = cv2.waitKey(2)

                # Select ROI
                if key == ord('s'):
                    self.selected_ROI = True
                    self.roi = cv2.selectROI(self.frame)

                # Close program with keyboard 'q'
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit(1)

                # Detect motion within ROI
                if self.selected_ROI:
                    x, y, w, h = self.roi
                    roi_frame = fgmask[y:y+h, x:x+w]
                    motion_detected = cv2.countNonZero(roi_frame)

                    if motion_detected > 0:
                        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Display frame
                cv2.imshow('image', self.frame)

            else:
                pass

if __name__ == '__main__':
    motion_detector = MotionDetector()
