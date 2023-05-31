> lidar.py
```python
from pop.LiDAR import Rplidar
import math
class Lidar:

    def __init__(self, length) :        # Turn On LiDAR 
        self.lidar = Rplidar()
        self.lidar.connect()
        self.lidar.startMotor()
        self.length = length
        print("Lidar Setup Complete")

    def __del__(self):                  # Turn Off LiDAR
        self.lidar.stopMotor()

    def __trans_steer(self, steering):
        return 90 * steering

    def check_distance(self, steering):
        detect = 0
        V = self.lidar.getVectors()
        sub_value = self.__trans_steer(steering)
        for degrees, distance, _ in V :
            if degrees > 0 + sub_value and degrees < 360 - sub_value:
                continue
            else :
                if distance < self.length[2]:
                    detect = 3
                    break
                elif distance < self.length[1] :
                    detect = 2
                    break
                elif distance < self.length[0]:
                    detect = 1
                    break
        print("detect %d"%(detect))     # Debug
        return detect
```     

> main.py
```python
# Import----------------------------------
from pop import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot
from lidar import Lidar
import time

print("Import Complete")
# ------------------------------------------

bot = None
of = None
lidar = None
person_not_found_cnt = 0
flag = 0
speed = 0

def setup():
    print("Setup Start")
    global bot, of, lidar
    
    length = [1000, 800, 600]   # 측정 거리
    
    cam = Camera()
    of = Object_Follow(cam)
    bot = SerBot()
    lidar = Lidar(length)

    of.load_model()
    print("="*50)
    print("Model load ok!")
    print("It starts in about 10 seconds.")

def loop():
    global person_not_found_cnt, flag, speed
    detect = lidar.check_distance(bot.steering)

    if detect != 3 :
        person = of.detect(index='person')
        if person:
            person_not_found_cnt = 15
            x = round(person['x'] * 4, 1)
            
            speed = 90 if detect == 0 else 60 if detect == 1 else 30
            bot.forward(speed)
            bot.steering = 1.0 if x > 1.0 else -1.0 if x < -1.0 else x
            flag = 0 if x < 0 else 1 
    
            print(f"{x}, {bot.steering}")            
        else:
            if person_not_found_cnt >= 10:
                bot.setSpeed(50)
                if flag:
                    bot.turnRight()
                    time.sleep(0.15)
                else :
                    bot.turnLeft()
                    time.sleep(0.15)
            else :
                person_not_found_cnt += 1
    else :
        print("Can't Move!")
        bot.stop()
 
def main():
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            break
    
    bot.stop()
    
if __name__ == '__main__':
    main()
    
``` 
