import cv2
import sys

haar_face = '/usr/local/share/opencv4/haarcascades/haarcascade_front alface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_face)

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Not found camera")
    sys.exit()

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.3,min Neighbors=1,minSize=(100,100))

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
     
    cv2.imshow('img',img)
    if cv2.waitKey(10) >= 0:
        break

cam.release()
cv2.destroyAllWindows()