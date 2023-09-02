# day3 - axis6

## timeit

IPython이 포함된 코드입니다.   
기초 인터럽트 제어 중 하나인 *타이머*입니다. Internal Interrupt가 있는 마이크로프로세서와는 달리, 고성능 프로세서 보드는 인터럽트를 잘 활용하기 힘듭니다.(애초에 레지스터단에 접근하기도 힘듭니다.) 이에 사용하는 라이브러리가 `timeit`입니다. 나름 일정한 시간 간격으로 프로그램에 확인 작업을 거칠 수 있으며, 비동기 작업을 진행할 수 있습니다. 

```py
#%%
import timeit
import time
# %%
p1 = timeit.default_timer()
time.sleep(1)
p2 = timeit.default_timer()
print(p2-p1)
# %%

```

## axis-6

6축 자이로의 데이터를 받고, 이를 동작하는 코드입니다. 첫 번째 코드는 IPython Widget을 통해 자이로 값을 시각적으로 확인할 수 있는 코드이고, 두 번째 코드는 이 데이터를 바탕으로 stabilizer를 만드는 코드입니다. 가변하는 Z축의 값을 실시간으로 측정하여 steering 값을 조정해줌으로써 직선 주행을 유지해줄 수 있습니다.

지금은 여러번의 테스트 끝에 임의의 데이터를 찾아가는 형태로 진행했지만, 추후 더욱 진행한다면 머신러닝을 활용하여 최적의 Steering 값을 탐색해줄 수 있을 것입니다.

```py
# test

#%%
import time
import ipywidgets as widgets
from threading import Thread
# %%
delay = widgets.IntSlider(max=1000, value=1, description='delay')
gyro = [widgets.FloatSlider(min=-90, max=90, description='gyro_'+s) for s in ('x', 'y', 'z')] #degree/s
accel = [widgets.FloatSlider(min=-12, max=12, step=0.01, description='accel_'+s) for s in ('x', 'y', 'z')] #m/s^2
display(delay)
for i in range(3):
    display(gyro[i])
for i in range(3):   
    display(accel[i])
# %%
is_imu_thread = True

from pop.Pilot import IMU, SerBot
imu = IMU()
bot = SerBot()

def onReadIMU():
    bot.setSpeed(50)
    bot.steering = 0.1
    bot.forward()
    while is_imu_thread:
        gyro[0].value, gyro[1].value, gyro[2].value = imu.getGyro().values()
        accel[0].value, accel[1].value, accel[2].value = imu.getAccel().values()

        if(gyro[2].value > 1.0 or gyro[2].value > -1.0):
            time.sleep(delay.value/1000)
    

Thread(target=onReadIMU).start()
# %%
bot.stop()
# %%
bot.turnLeft()
# %%
```

```py
# Movement

#%%
from pop.Pilot import SerBot
from pop.Pilot import IMU
import timeit

#%%
bot = SerBot()
imu = IMU()

bot.setSpeed(50)

#%%
bot.steering = 0.0
bot.forward()
p0= timeit.default_timer()
p1= timeit.default_timer()
s0= timeit.default_timer()

s = False

while True:
    current = timeit.default_timer()
    
    if current - p0 > 11.75 :
        break

    if(s and current - s0 > 0.004) :
        s = False
        bot.steering = 0.0

    if current - p1 > 0.0075:
        p1 = timeit.default_timer()
        if tuple(imu.getGyro().values())[2] > 0.8:
            bot.steering = 0.15
            s= True
            s0 = timeit.default_timer()
        elif tuple(imu.getGyro().values())[2] < -0.8:
            bot.steering = -0.15
            s= True
            s0 = timeit.default_timer()

bot.stop()
#%%
bot.stop()
# %%
```