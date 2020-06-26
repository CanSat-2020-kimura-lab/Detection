import time 
import datetime
import pigpio
from threading import Thread

#-- GPIO connection --#
Ena1 = 12
Pha1 = 21
Ena2 = 1
Pha2 = 1

LARGE = 8
MODE = 7
STBY = 18

#-- モーターはOUT1とOUT2、OUT3とOUT4で一つずつ接続されている --#

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
#--- GPS ---#
pi.set_mode(RX,pigpio.INPUT)

def setup_mode(a,b,c):
    pi.write(MODE,a)
    pi.write(LARGE,b)
    pi.write(STBY,c)

def setup_IN(d,e,f,g):
    pi.write(Ena1,d)
    pi.write(Pha1,e)
    pi.write(Ena2,f)
    pi.write(Pha2,g)

#-- run phase definition --#
class Run:
    def straight(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,1)
        #setup_OUT(1,0,1,0)
    
    def back(self):
        setup_mode(1,0,1)
        setup_IN(1,0,1,0)
        #setup_OUT(0,1,0,1)
    
    def rotation(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,0)
        #setup_OUT(1,0,0,1)
    
    def stop(self):
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)

    def turn_right(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)
        time.sleep(1)
        #-- rotate only right wheel --#
        setup_mode(1,0,1)
        setup_IN(1,1,1,1)
        #setup_OUT(1,1,0,0)
       
    def turn_left(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)
        time.sleep(1)
        #-- rotate only left wheel --#
        setup_mode(1,0,1)
        setup_IN(1,1,1,1)
        #setup_OUT(0,0,1,1)

start = time.time
 

while True:
    now = time.time
    t = now - start
    if t < 5:
        run = Run()
        run.straight()
