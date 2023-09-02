# day2 - dawit-star

인공지능의 가장 대표, 선형 머신러닝의 기본 원리를 이해하는 과정입니다. 일정한 속도에서 특정한 각도에 도달하는 시간을 측정하고, 이를 그래프로 표현 한 뒤 하나의 직선방정식을 구합니다. 이를 이용해서 SerBot 기존에 없던 기능인, 특정 각도에 도달하는 기능을 만들 수 있습니다.

```py
# SerBotEx
from pop.Pilot import SerBot
import time

class SerBotEx(SerBot):
    def __calc_delay(self, n):
        speed = self.getSpeed()

        if speed <= 20:
            d = n/90 - (n/90) * 0.0
        elif speed <= 40 :
            d = n/90 - (n/90) * 0.4
        elif speed <= 60:
            d = n/90 - (n/90) * 0.6
        elif speed <= 80:
            d = n/90 - (n/90) * 0.7
        elif speed <= 100:
            d = n/90 - (n/90) * 0.76

        return d


    def turnAngleLeft(self, n):
        d = self.__calc_delay(n)
        self.turnLeft()
        time.sleep(d)
        self.stop()

    def turnAngleRight(self, n):
        d = self.__calc_delay(n)
        self.turnRight()
        time.sleep(d)
        self.stop()

    def turnAngleLeftSam(self, n):
        self.turnLeft()
        time.sleep(n*0.006125)

ser = SerBotEx(SerBot)

ser.setSpeed(50)

ser.turnAngleLeft(60)
```

```py
from day2 import SerBotEx
from pop.Pilot import SerBot
import time
import turtle as t

ser = SerBotEx(SerBot)

ser.setSpeed(50)


def makeSharp():
    ser.forward()
    time.sleep(1)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(1)
    ser.stop()
    ser.turnAngleRight(60)
    
def makeTri1() :
    ser.forward()
    time.sleep(1)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(3)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(3)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(2)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)

def makeTri2() :
    ser.forward()
    time.sleep(2)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(3)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(3)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)
    ser.forward()
    time.sleep(1)
    ser.stop()
    ser.turnAngleLeftSam(60)
    ser.turnAngleLeftSam(60)




ser.steering = 0

'''
for i in range(6):
    makeSharp()
'''

makeTri1()
makeTri2()
    
ser.stop()
```