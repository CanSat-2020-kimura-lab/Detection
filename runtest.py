import time 
import datetime
import pigpio
from threading import Thread

#-- GPIO connection --#
Ena1 = 13
Pha1 = 19
Ena2 = 12
Pha2 = 25

LARGE = 10
MODE = 9
STBY = 11

pi = pigpio.pi()

#--- Set the GPIO_mode ---#
#--- Motor ---#
pi.set_mode(Ena1, pigpio.OUTPUT)
pi.set_mode(Pha1,pigpio.OUTPUT)
pi.set_mode(Ena2, pigpio.OUTPUT)
pi.set_mode(Pha2,pigpio.OUTPUT)
pi.set_mode(MODE,pigpio.OUTPUT)
pi.set_mode(LARGE,pigpio.OUTPUT)
pi.set_mode(STBY,pigpio.OUTPUT)

def setup_mode(a,b,c):
    pi.write(MODE,a)
    pi.write(LARGE,b)
    pi.write(STBY,c)

def setup_IN(d,e,f,g,t):
    pi.write(Ena1,d)
    pi.write(Pha1,e)
    pi.write(Ena2,f)
    pi.write(Pha2,g)
    time.sleep(t)

#-- run phase definition --#
class Run:
    def straight(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,1,2.0)

    def back(self):
        setup_mode(1,0,1)
        setup_IN(1,0,1,0,2.0)

    def rotation(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,0,2.0)
    
    def stop(self):
        setup_mode(1,0,1)
        setup_IN(0,0,0,0,2.0)

    def turn_right(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0,1.0)
        #-- rotate only right wheel --#
        setup_mode(1,0,1)
        setup_IN(1,1,1,1,2.0)
      
    def turn_left(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0,2.0)
        time.sleep(1)
        #-- rotate only left wheel --#
        setup_mode(1,0,1)
        setup_IN(1,1,1,1,2.0)

start = time.time()

#-- Timer --#
cond = True

def timer():
    global cond
    time.sleep(3)
    cond = False
'''
while True:
    try :
        now = time.time()
        t = now - start
        run = Run()
        run.straight()
        if t > 3:
            run = Run()
            run.stop()
            break
    except KeyboardInterrupt:
        run = Run()
        run.stop()
'''
try:
    while cond:
        run = Run()
        run.straight()

except KeyboardInterrupt:
        run = Run()
        run.stop()
        
finally:
    run = Run()
    run.stop()
