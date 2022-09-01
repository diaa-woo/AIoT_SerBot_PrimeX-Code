import cv2
import numpy as np

# Blue
#lowerBound=np.array([97,100,117])
#upperBound=np.array([117,255,255])
# RED
lowerBound=np.array([170,50,0])
upperBound=np.array([179,255,255])
# Green
#lowerBound=np.array([50,100,100])
#upperBound=np.array([70,255,255])

cam= cv2.VideoCapture(1)

if cam.isOpened() == False: 
    print ('Can\'t open the CAM(%d)' % (1))
    exit()

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

while True:
    ret, img=cam.read()

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskFinal=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    h,conts,_=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)

    cv2.imshow("Color_Detection",img)
    if cv2.waitKey(10) >= 0:
        break;
cv2.destroyAllWindows()
