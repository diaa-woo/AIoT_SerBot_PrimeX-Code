from pop import Pilot

cam=Pilot.Camera(width=300, height=300)
bot=Pilot.SerBot()

OF=Pilot.Object_Follow(cam)
OF.load_model()

while True:
    v=OF.detect(index='person')
    
    if v is not None:
        steer=v['x']*4
        
        if steer > 1:
            steer=1
        elif steer < -1 :
            steer=-1
            
        bot.steering=steer
        
        if v['size_rate']<0.20:
            bot.forward(50)
        else:
            bot.stop()
        
    else:
        bot.stop()