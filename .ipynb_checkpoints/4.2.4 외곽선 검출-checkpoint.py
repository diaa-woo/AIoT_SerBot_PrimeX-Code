import cv2
import sys

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Not found camera")
    sys.exit()

while True:
    ret, frame = cap.read()
    img = cv2.Canny(frame,100, 200)
    
    cv2.imshow("soda", img)

    if cv2.waitKey(1) == ord('q'):
        break