from pop import Pilot
import cv2

cam=Pilot.Camera(width=320, height=320)
bot=Pilot.SerBot()
OF=Pilot.Object_Follow(cam)
OF.load_model()

cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)
cv2.resizeWindow(winname='image', width=600, height=600)
cv2.moveWindow(winname='image', x=200, y=25)

while cv2.waitKey(10) < 0:
    v=OF.detect(index='person')
    
    img = cam.value
    cv2.imshow("image", img)
    
    if v is not None:
        steer=-v['x']*4
        if steer > 1:
            steer=1
        elif steer < -1:
            steer=-1
        bot.steering=-steer
        if v['size_rate']<0.20:
            bot.forward(50)
        else:
            bot.stop()
    else:
        bot.stop()
        
cv2.destroyAllWindows()