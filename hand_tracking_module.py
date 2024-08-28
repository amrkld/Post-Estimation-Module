import cv2
import mediapipe as mp
import time


class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.pTime = 0

    def process_frame(self, id_num):
        success, img = self.cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            return

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == id_num:  # Index for thumb tip
                        cv2.circle(img, (cx, cy), 15, (225, 0, 225), cv2.FILLED)
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)


        # Calculate and display frame rate
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, f'{int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("Image", img)


    def run(self):
        while True:
            self.process_frame(4)
            # If the user presses the ESC key or closes the window, exit loop
            if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
                break
            if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release the capture and destroy all OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    hand_tracker = HandTracker()
    hand_tracker.run()
