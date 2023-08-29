# Bot Move

> move.py
```python
from pop import Pilot
import time

bot = Pilot.SerBot()    # 로봇의 기본 동작 모듈 import
bot.setSpeed(30)        # 기본 속도 결정

bot.forward(50)         # 앞으로
time.sleep(1)
bot.turnRight()         # 제자리 우회전
time.sleep(1.5)
bot.backward(50)        # 뒤로
time.sleep(1)

bot.stop()              # 정지
```