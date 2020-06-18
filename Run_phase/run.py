import sys
#-- ラズパイから各プログラムのパスを通す --#
sys.path.append()
sys.path.append()
sys.path.append()

import GPS
import moter
import Wireless

import time 
import datetime
import pigpio
import serial
from threading import Thread

#-- GPIO connection --#
Ena1 = 12
Pha1 = 21
Ena2 = 1
Pha2 = 1
OUT1 = 1
OUT2 = 1
OUT3 = 1
OUT4 = 1
LARGE = 8
MODE = 7
STBY = 18

RX = 26

#-- モーターはOUT1とOUT2、OUT3とOUT4で一つずつ接続されている --#

pi = pigpio.pi()

#-- Set the GPIO_mode --#
pi.set_mode(Ena1, pigpio.OUTPUT)
pi.set_mode(Pha1,pigpio.OUTPUT)
pi.set_mode(Ena2, pigpio.OUTPUT)
pi.set_mode(Pha2,pigpio.OUTPUT)
pi.set_mode(MODE,pigpio.OUTPUT)
pi.set_mode(LARGE,pigpio.OUTPUT)
pi.set_mode(STBY,pigpio.OUTPUT)

pi.set_mode(RX,pigpio.OUTPUT)
'''
pi.write(22,1)  #Wireless.SW:ON
'''

#-- GPS data --#


#-- motor mode control definition --#
def setup_mode(a,b,c):
    pi.write(MODE,a)
    pi.write(LARGE,b)
    pi.write(STBY,c)

def setup_IN(d,e,f,g):
    pi.write(Ena1,d)
    pi.write(Pha1,e)
    pi.write(Ena2,f)
    pi.write(Pha2,g)

def setup_OUT(h,i,j,k):
    pi.write(OUT1,h)
    pi.write(OUT2,i)
    pi.write(OUT3,j)
    pi.write(OUT4,k)

#-- run phase definition --#
class Run:
    def straight(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,1)
        setup_OUT(1,0,1,0)
    
    def back(self):
        setup_mode(1,0,1)
        setup_IN(1,0,1,0)
        setup_OUT(0,1,0,1)
    
    def rotation(self):
        setup_mode(1,0,1)
        setup_IN(1,1,1,0)
        setup_OUT(1,0,0,1)
    
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
        setup_OUT(1,1,0,0)
       
    def turn_left(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)
        time.sleep(1)
        #-- rotate only left wheel --#
        setup_mode(1,0,1)
        setup_IN(1,1,1,1)
        setup_OUT(0,0,1,1)
        time

#-- obtain calculated data from GPS-Navigate.py --#
def gps_data():
    print('距離:{}'.s)
    print('方位角(始点⇒終点):', degrees(α1) )
    print('方位角(終点⇒始点):', degrees(α2) )

#-- note start time  --#
start_time = datetime.datetime
print(start_time)
time_log = time.time

cond = True

def timer():
    global cond
    time.sleep(5)
    cond = False

#-- run by GPS guide if we aren't within 5m from the goal --#
while s>5:
    #-- 進行方向がゴール方向になるまで回転制御 --#
    if α1 != 0:
        while True:
            gps_data()
            run = Run()
            run.turn_left()

            if α1 == 0:
                break   # escape from while loop
    
    #-- run phase --#
    while True:
        run.straight()
        now = time.time
        print(now)
        #-- stop to calibration if 60 seconds have passed since the last calibration --#
        if now - time_log >= 60:
            run = Run()           
            run.stop()
            time.sleep(5)
            thread = Thread(target=timer)
            thread.start()
            #-- calibration --#
            while cond:
                run.rotation()
            
            time.sleep(3)
            #-- 進行方向がゴール方向になるまで回転制御 --#
            if α1 != 0:
                while True:
                    gps_data()
                    run = Run()
                    run.turn_left()

                    if α1 == 0:
                        break   # escape from while loop
    
            #-- note time which last claibration was finished--#    
            global time_log
            time_log = time.time
            print(time_log)
