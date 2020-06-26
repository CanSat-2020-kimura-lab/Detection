import time 
import pigpio
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

pi = pigpio.pi()

#-- Set the GPIO_mode --#
pi.set_mode(Ena1, pigpio.OUTPUT)
pi.set_mode(Pha1,pigpio.OUTPUT)
pi.set_mode(Ena2, pigpio.OUTPUT)
pi.set_mode(Pha2,pigpio.OUTPUT)
pi.set_mode(MODE,pigpio.OUTPUT)
pi.set_mode(LARGE,pigpio.OUTPUT)
pi.set_mode(STBY,pigpio.OUTPUT)

#-- frequency --#
freq = 50
#-- frequency range --#
range =255   # 25 ~ 40000

pi.set_PWM_frequency(Ena1,freq)
pi.set_PWM_frequency(Pha1,freq)
pi.set_PWM_frequency(Ena2,freq)
pi.set_PWM_frequency(Pha2,freq)

pi.set_PWM_range(Ena1,range)
pi.set_PWM_range(Pha1,range)
pi.set_PWM_range(Ena2,range)
pi.set_PWM_range(Pha2,range)

#-- PWM control --#
#-- duty ratio --#
# duty比の最大は range の最大から考える
d = 0
def high_speed():
    global d
    d = 192  # duty ratio = 3/4
    '''
    pi.set_PWM_dutycycle(Ena1, d)
    pi.set_PWM_dutycycle(Pha1, d)
    pi.set_PWM_dutycycle(Ena2, d)
    pi.set_PWM_dutycycle(Pha2, d)
    '''

def normal_speed():
    global d
    d = 128  # duty ratio = 1/2
    '''
    pi.set_PWM_dutycycle(Ena1, d)
    pi.set_PWM_dutycycle(Pha1, d)
    pi.set_PWM_dutycycle(Ena2, d)
    pi.set_PWM_dutycycle(Pha2, d)
    '''

def low_speed():
    global d
    d = 64  # duty ratio = 1/4
    '''
    pi.set_PWM_dutycycle(Ena1, d)
    pi.set_PWM_dutycycle(Pha1, d)
    pi.set_PWM_dutycycle(Ena2, d)
    pi.set_PWM_dutycycle(Pha2, d)
    '''

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
'''
def setup_OUT(h,i,j,k):
    pi.write(OUT1,h)
    pi.write(OUT2,i)
    pi.write(OUT3,j)
    pi.write(OUT4,k)
'''
#-- run phase definition --#
class Run:
    def straight_h(self):
        high_speed()
        setup_mode(1,0,1)

        pi.set_PWM_dutycycle(Ena1, d)
        pi.set_PWM_dutycycle(Pha1, d)
        pi.set_PWM_dutycycle(Ena2, d)
        pi.set_PWM_dutycycle(Pha2, d)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''

        setup_IN(d,d,d,d)
        #setup_OUT(d,0,d,0)
        #setup_IN(1,1,1,1)
        #setup_OUT(1,0,1,0)

    def straight_l(self):
        low_speed()
        setup_mode(1,0,1)

        pi.set_PWM_dutycycle(Ena1, d)
        pi.set_PWM_dutycycle(Pha1, d)
        pi.set_PWM_dutycycle(Ena2, d)
        pi.set_PWM_dutycycle(Pha2, d)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''

        setup_IN(d,d,d,d)
        #setup_OUT(d,0,d,0)
        #setup_IN(1,1,1,1)
        #setup_OUT(1,0,1,0)

    
    def back(self):
        high_speed()
        setup_mode(1,0,1)

        pi.set_PWM_dutycycle(Ena1, d)
        pi.set_PWM_dutycycle(Pha1, d)
        pi.set_PWM_dutycycle(Ena2, d)
        pi.set_PWM_dutycycle(Pha2, d)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''

        setup_IN(d,0,d,0)
        #setup_OUT(0,d,0,d)
        #setup_IN(1,0,1,0)
        #setup_OUT(0,1,0,1)
    
    def rotation(self):
        high_speed()
        setup_mode(1,0,1)

        pi.set_PWM_dutycycle(Ena1, d)
        pi.set_PWM_dutycycle(Pha1, d)
        pi.set_PWM_dutycycle(Ena2, d)
        pi.set_PWM_dutycycle(Pha2, d)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''

        setup_IN(d,d,d,0)
        #setup_OUT(d,0,0,d)
        #setup_IN(1,1,1,0)
        #setup_OUT(1,0,0,1)
    
    def stop(self):
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)

    def turn_right(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)
        time.sleep(1)
        #-- right wheel is high speed left wheel is low speed --#
        high_speed()
        d1 = d
        low_speed()
        d2 = d
        setup_mode(1,0,1)
        pi.set_PWM_dutycycle(Ena1, d1)
        pi.set_PWM_dutycycle(Pha1, d1)
        pi.set_PWM_dutycycle(Ena2, d2)
        pi.set_PWM_dutycycle(Pha2, d2)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''
        setup_IN(d1,d1,d2,d2)
        #setup_OUT(d,0,d,0)

        #-- rotate only right wheel --#
        #setup_IN(1,1,1,1)
        #setup_OUT(1,1,0,0)
       
    def turn_left(self):
        #-- stop --#
        setup_mode(1,0,1)
        setup_IN(0,0,0,0)
        time.sleep(1)
        #-- right wheel is high speed left wheel is low speed --#
        low_speed()
        d1 = d
        high_speed()
        d2 = d
        setup_mode(1,0,1)
        pi.set_PWM_dutycycle(Ena1, d1)
        pi.set_PWM_dutycycle(Pha1, d1)
        pi.set_PWM_dutycycle(Ena2, d2)
        pi.set_PWM_dutycycle(Pha2, d2)
        '''
        pi.set_PWM_dutycycle(OUT1, d)
        pi.set_PWM_dutycycle(OUT2, d)
        pi.set_PWM_dutycycle(OUT3, d)
        pi.set_PWM_dutycycle(OUT4, d)
        '''
        setup_IN(d,d,d,d)
        #setup_OUT(0,0,d,d)
        #setup_IN(1,1,1,1)
        #setup_OUT(0,0,1,1)

time_log = time.time
print(time_log)

def timer():
    global cond
    time.sleep(5)
    cond = False

run = Run()

#-- Run test --#
thread = Thread(target = timer)
thread.start()
#-- run straight at high speed for 5 seconds --#
while cond:
    run. straight_h()
time.sleep(5)

thread = Thread(target = timer)
thread.start()
#-- run straight at low speed  for 5 seconds --#
while cond:
    run. straight_l()
time.sleep(5)

thread = Thread(target = timer)
thread.start()
#-- run back for 5 seconds --#
while cond:
    run.back()
time.sleep(5)

thread = Thread(target = timer)
thread.start()
#-- rotation for 5 seconds --#
while cond:
    run.rotation()
time.sleep(5)

thread = Thread(target = timer)
thread.start()
#-- turn right for 5 seconds --#
while cond:
    run. turn_right()
time.sleep(5)

thread = Thread(target = timer)
thread.start()
#-- turn left for 5 seconds --#
while cond:
    run. turn_left()
time.sleep(5)