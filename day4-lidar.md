# day4 - lidar

Lidar 변경 코드입니다.

```py
from pop.LiDAR import Rplidar
import math

class Lidar:
    def __init__(self, width, directions):
        self.serbot_width = width
        self.degrees = list(range(0, 360, 360 // directions))

        self.lidar = Rplidar()
        self.lidar.connect()
        self.lidar.startMotor()

    def __del__(self):
        self.lidar.stopMotor()

    def __calcAngle(self, length):
        tan = (self.serbot_width / 2) / length
        angle = math.atan(tan) * (180 / math.pi)
        return angle

    def collisonDetect(self, length):
        detect = [0] * len(self.degrees)
        angle = self.__calcAngle(length)
        ret = self.lidar.getVectors()
        for degree, distance, _ in ret:
            for i, detect_direction in enumerate(self.degrees):
                min_degree = (detect_direction - angle) % 360
                if (degree + (360 - min_degree)) % 360 <= (angle * 2):
                    if distance < length:
                        detect[i] = 1
                        break
        return detect
```

IPython Widget을 이용해서 Lidar 값을 확인할 수 있는 코드입니다.

```py
from pop.LiDAR import Rplidar
import matplotlib.pyplot as plt
import numpy as np
import cv2

lidar = Rplidar()
lidar.connect()
lidar.startMotor()

fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
ax = fig.add_subplot(111, projection='polar')
fig.tight_layout()

dist = 5000 #5m

while True:
    V = np.array(lidar.getVectors(True))
    V = np.where(V <= dist, V, 0)
    ax.plot(np.deg2rad(V[:,0]), V[:,1])
    fig.canvas.draw()

    cv2.imshow("lidar", np.array(fig.canvas.renderer._renderer))
    plt.cla()
    ax.set_theta_zero_location("N")

    if cv2.waitKey(3) == 27:
        break

lidar.stopMotor()
cv2.destroyAllWindows()
```

전방에 있는 장애물을 파악하고 고정축 이동을 통해 장애물을 회피하는 코드입니다.

```py
from pop.Pilot import SerBot
from lidar import Lidar
import time

def main() :
    serbot_width = 500
    direction_count = 36
    speed = 50

    bot = SerBot() 
    lidar = Lidar(serbot_width, direction_count)
    flag = True

    print("Start!")

    bot.setSpeed(speed)
    bot.forward()

    while flag:
        try :  
            detect = lidar.collisonDetect(1500)

            if sum(detect) == direction_count:
                # 모든 방향에서 장애물을 감지하지 않으면 전진합니다.
                bot.steering = 0
                bot.forward()
                continue

            if detect[0] == 1 or detect[1] == 1:
                if detect[2] or detect[3]:
                    # 왼쪽으로 회피합니다.
                    bot.steering = -0.8
                    time.sleep(1.5)
                    bot.steering = 0.8
                    time.sleep(3)
                    bot.steering = -0.8
                    time.sleep(1.5)
                    bot.steering = 0
                    continue
                elif detect[34] or detect[35]:
                    # 오른쪽으로 회피합니다.
                    bot.steering = 0.8
                    time.sleep(1.5)
                    bot.steering = -0.8
                    time.sleep(3)
                    bot.steering = 0.8
                    time.sleep(1.5)
                    bot.steering = 0
                    continue

            # 만약 모든 조건에 해당되지 않으면 전진합니다.
            bot.steering = 0
            bot.forward()
        
        except (KeyboardInterrupt, SystemError):
            flag = False
    
    bot.stop()
    print('Stopped Serbot!')

if __name__ == '__main__':
    main()
```



