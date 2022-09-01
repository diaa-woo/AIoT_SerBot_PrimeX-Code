import can
import time
from threading import Thread
#TEST
class Can():
    def __init__(self):
        self._bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    
    def __del__(self):
        self._bus = 0

    def write(self, msg_id, buf, is_extended=False):
        msg = can.Message(arbitration_id=msg_id,is_extended_id=is_extended,data=buf)
        try:
            self._bus.send(msg)
            time.sleep(0.005)
        except can.CanError:
            print("Can Interface Message does not Send")

    def read(self,timeOut=2):
        recv_buf = self._bus.recv(timeout=timeOut)
        if recv_buf:
            return recv_buf

    def setFilter(self, can_id, mask):
        self._bus.set_filters([{"can_id": can_id, "can_mask": mask, "extended": False}])

class OmniWheel(Can):
    MOTOR_CONTROL       =   0x101
    MOTOR_STOP          =   0x102
    SENSOR_REQUEST      =   0x103
    OBSTACLE_DISTANCE   =   0x104
    OBSTACLE_DETECT     =   0x133
    OBSTACLE_ALARM      =   0x134
    RECV_ULTRASONIC     =   0x135
    RECV_PSD            =   0x136
    ULTRASONIC          =   0x001
    PSD                 =   0x002
    ALARM               =   0x003
    SENSOR_ALL          =   0x004

    def __init__(self):
        super().__init__()
        self._ultraEnable = 0x0
        self._psdEnable = 0x0
        self._ultraData = [0,0,0,0,0,0]
        self._psdData = [0,0,0]
        self._alarm = [0,0,0,0,0,0,0,0,0]
        self._func = None
        self._param = None
        self._wheels = [0,0,0,0,0,0]

        Can.setFilter(self,0x130,0x7F0)
        self.allSensorEnable()
        self.readStart()

    def __del__(self):
        super().__del__()

    def wheel(self, id, value):
        if id == 1 :
            if value < 0 :
                self._wheels[0]=int(abs(value))
                self._wheels[1]=0
            elif value > 0 :
                self._wheels[0]=0
                self._wheels[1]=int(abs(value))
            else :
                self._wheels[0]=0
                self._wheels[1]=0
        elif id == 2 :
            if value < 0 :
                self._wheels[2]=int(abs(value))
                self._wheels[3]=0
            elif value > 0 :
                self._wheels[2]=0
                self._wheels[3]=int(abs(value))
            else :
                self._wheels[2]=0
                self._wheels[3]=0
        elif id == 3 :
            if value < 0 :
                self._wheels[4]=int(abs(value))
                self._wheels[5]=0
            elif value > 0 :
                self._wheels[4]=0
                self._wheels[5]=int(abs(value))
            else :
                self._wheels[4]=0
                self._wheels[5]=0
        time.sleep(0.01)
        Can.write(self,self.MOTOR_CONTROL,self._wheels)

    def forward(self, data=None):
        if data is None:
            Can.write(self,self.MOTOR_CONTROL,self._wheels)
        else:
            Can.write(self,self.MOTOR_CONTROL,[data[0],0,data[1],0,data[2],0])

    def backward(self, data=None):
        if data is None:
            tmp=self._wheels[:]
            tmp=tmp[0:2][::-1]+tmp[2:4][::-1]+tmp[4:6][::-1]
            Can.write(self,self.MOTOR_CONTROL,tmp)
        else:
            Can.write(self,self.MOTOR_CONTROL,[0,data[0],0,data[1],0,data[2]])

    def setObstacleRange(self, ultra_distance, psd_distance):
        Can.write(self,self.OBSTACLE_DISTANCE,[ultra_distance,psd_distance,0,0,0,0])

    def stop(self):
        Can.write(self,self.MOTOR_STOP,[0,0,0,0,0,0])

    def allSensorEnable(self):
        self._ultraEnable = 0x3F
        self._psdEnable = 0x7
        Can.write(self,self.SENSOR_REQUEST,[self._ultraEnable,self._psdEnable])

    def ultraEnable(self,enable=[1,1,1,1,1,1]):
        for i in range(6):
            if enable[i] == 1:
                self._ultraEnable = self._ultraEnable | (0x1 << i) 
            elif enable[i] == 0:
                self._ultraEnable = self._ultraEnable & ~(0x1 << i) 
            else:
                pass

        Can.write(self,self.SENSOR_REQUEST,[self._ultraEnable,self._psdEnable])

    def psdEnable(self,enable=[1,1,1]):
        for i in range(3):
            if enable[i] == 1:
                self._psdEnable = self._psdEnable | (0x1 << i) 
            elif enable[i] == 0:
                self._psdEnable = self._psdEnable & ~(0x1 << i) 
            else:
                pass

        Can.write(self,self.SENSOR_REQUEST,[self._ultraEnable,self._psdEnable])

    def getEnable(self):
        return self._ultraEnable, self._psdEnable

    def sensorDisable(self):
        self._ultraEnable = 0x0
        self._psdEnable = 0x0
        Can.write(self,self.SENSOR_REQUEST,[self._ultraEnable,self._psdEnable])

    def _readSensor(self):
        while True:
            recv_data = Can.read(self)
            try:
                if recv_data.arbitration_id == self.RECV_ULTRASONIC:
                    for i in range(6):
                        self._ultraData[i] = int(recv_data.data[i])
                elif recv_data.arbitration_id == self.RECV_PSD:
                    for i in range(3):
                        self._psdData[i] = int(recv_data.data[i])
                elif recv_data.arbitration_id == self.OBSTACLE_ALARM and recv_data.dlc == 2:
                    self._alarm[0] = 1
                    for i in range(2):
                        self._alarm[i+1] = int(recv_data.data[i])
                elif recv_data.arbitration_id == self.OBSTACLE_DETECT or recv_data.dlc == 8:
                    self._alarm[0] = 2 
                    for i in range(8):
                        self._alarm[i+1] = int(recv_data.data[i])
                else:
                    print("wrong message recvd..")
            except: 
                pass
            time.sleep(0.1)

    def readStart(self):
        if not hasattr(self, 'read_thread') or not self.read_thread.isAlive():
            self.read_thread = Thread(target=self._readSensor)
            self.read_thread.start()

    def readStop(self):
        if hasattr(self, 'thread'):
            self.thread.join()

    def read(self,msgType=SENSOR_ALL):
        if msgType == self.ULTRASONIC:
            return self._ultraData
        elif msgType == self.PSD:
            return self._psdData
        elif msgType == self.ALARM:
            return self._alarm
        elif msgType == self.SENSOR_ALL:
            return self._ultraData, self._psdData

    def setCallback(self, func, param=None):
        self._func = func 
        self._param = param
        if not hasattr(self, 'callback_thread') or not self.callback_thread.isAlive():
            self.callback_thread = Thread(target=self._func)
            self.callback_thread.start() if (self._func != None) else self.callback_thread.stop()

    
class Car:
    __steer_range=18
    
    def __init__(self):
        self.__can=Can()
        
    def wheel(self, value):
        data=[0,0]
        
        if abs(value)>100:
            value=100*abs(value)/value
            
        if value>0:
            data[0]=value
        elif value<0:
            data[1]=abs(value)
            
        self.__can.write(0x101, data)
        
    def steer(self, value):
        if abs(value)>1:
            value=abs(value)/value
            
        data=[int(90-self.__steer_range*value)]
        self.__can.write(0x102, data)
        
    def camPan(self, value):
        if abs(value)>60:
            value=60*abs(value)/value
            
        data=[int(90-value)]
        
        self.__can.write(0x103,data)
        
    def camTilt(self, value):
        if value<0: value=0
        elif value>90: value=90
            
        value*=0.744444
        
        data=[int(23+value)]
        
        self.__can.write(0x104,data)
            
    def ultraEnable(self,enable=[[1,1,1,1,1],[1,1,1,1,1]]):
        data=[]
        for n in range(2):
            value=0
            for i in range(5):
                if enable[n][i] == 1:
                    value|=(1<<i) 
                elif enable[n][i] == 0:
                    value&=~(1<<i) 
                else:
                    pass
            data.append(value)

        self.__can.write(0x105,data)