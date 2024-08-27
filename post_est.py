import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture("videos/video_01.mp4")

"""
# We can cap the video from a webcam by
cap = cv2.VideoCapture(0)

"""
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while(True):
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        #customize circles
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)


    #calc and print the frame rate
    ctime = time.time()
    fps = 1 / (ctime - pTime)
    pTime = ctime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    cv2.imshow("Image", img)


    #If clicks esc key
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
        break
    
    #check if the window is closed
    if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the capture and destroy any OpenCV windows
cap.release()
cv2.destroyAllWindows()