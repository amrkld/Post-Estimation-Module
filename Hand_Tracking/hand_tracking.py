import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
while True:
    sucess, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w) ,int(lm.y *h)
                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (225, 0, 225), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

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