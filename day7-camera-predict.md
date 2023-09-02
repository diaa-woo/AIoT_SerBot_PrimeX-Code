# day7 - Camera-Predict

YOLOv4 모델을 로드한 뒤, 미리 등록되어있는 사람 인식 모델을 호출한 후 카메라로 사람의 위치를 파악해 출력하는 코드입니다. 이 코드를 활용하면 사람을 따라다니는 예제를 만들 수 있습니다.

```py
# Print Human location

from pop.Pilot import Camera
from pop.AI import Object_Follow
import time

cam = Camera()
of = Object_Follow(cam)

of.load_model()
print('='*50)
print("Model load ok!")
print("It Starts in about 10 Seconds!")

while True:
    person = of.detect(index='person')
    if person:
        print(round(person['x'], 1), round(person['size_rate'], 1))
    time.sleep(0.5)
```

```py
# Move

from pop.Pilot import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot

cam = Camera()
of = Object_Follow(cam)
bot = SerBot()
bot.setSpeed(50)

of.load_model()
print('='*50)
print("Model load ok!")
print("It Starts in about 10 Seconds!")

#flag 변수 필요!
flag = 0
missingCount = 0

try:
    while True:
        person = of.detect(index='person')
        if person:
            bot.forward()
            missingCount = 0
            print(round(person['x'], 1), round(person['size_rate'], 1))
            steer = round(person['x'] * 3.5, 1)
            limit = round(person['size_rate'], 1)

            bot.steering = -1.0 if steer < -1.0 else 1.0 if steer > 1.0 else steer
            flag = 0 if steer < 0 else 1 

            if limit < 0.2:
                bot.stop()
        else:
            if missingCount >= 10:
                if flag:
                    bot.turnRight()
                else :
                    bot.turnLeft()
            else :
                missingCount += 1
except KeyboardInterrupt:
    bot.stop()
```