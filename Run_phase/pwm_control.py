import time 
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

#--- PWM control ---#
#--- duty ratio (duty ration = d/range) ---#
d = 0
def high_speed():
        global d
        d = 255  # duty ratio = 3/4

def normal_speed():
        global d
        d = 128  # duty ratio = 1/2

def low_speed():
        global d
        d = 64  # duty ratio = 1/4

#--- motor mode control definition ---#
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

#--- run phase definition ---#
class Run:
        def straight_h(self):
                high_speed()
                setup_mode(1,0,1)

                pi.set_PWM_dutycycle(Ena1, d)
                pi.set_PWM_dutycycle(Pha1, d)
                pi.set_PWM_dutycycle(Ena2, d)
                pi.set_PWM_dutycycle(Pha2, d)

                #setup_IN(1,1,1,1)
                #setup_OUT(1,0,1,0)

        def straight_n(self):
                normal_speed()
                setup_mode(1,0,1)

                pi.set_PWM_dutycycle(Ena1, d)
                pi.set_PWM_dutycycle(Pha1, d)
                pi.set_PWM_dutycycle(Ena2, d)
                pi.set_PWM_dutycycle(Pha2, d)

                #setup_IN(1,1,1,1)
                #setup_OUT(1,0,1,0)

        def straight_l(self):
                low_speed()
                setup_mode(1,0,1)

                pi.set_PWM_dutycycle(Ena1, d)
                pi.set_PWM_dutycycle(Pha1, d)
                pi.set_PWM_dutycycle(Ena2, d)
                pi.set_PWM_dutycycle(Pha2, d)

                #setup_IN(1,1,1,1)
                #setup_OUT(1,0,1,0)
        
        def back(self):
                high_speed()
                setup_mode(1,0,1)

                pi.set_PWM_dutycycle(Ena1, d)
                #pi.set_PWM_dutycycle(Pha1, d)
                pi.set_PWM_dutycycle(Ena2, d)
                #pi.set_PWM_dutycycle(Pha2, d)

                #setup_IN(1,0,1,0)
                #setup_OUT(0,1,0,1)
        
        def rotation(self):
                high_speed()
                setup_mode(1,0,1)

                pi.set_PWM_dutycycle(Ena1, d)
                pi.set_PWM_dutycycle(Pha1, d)
                pi.set_PWM_dutycycle(Ena2, d)
                #pi.set_PWM_dutycycle(Pha2, d)

                #setup_IN(1,1,1,0)
                #setup_OUT(1,0,0,1)
        
        def stop(self):
                setup_mode(1,0,1)
                setup_IN(0,0,0,0,1.0)

        def turn_right(self):
                #-- right wheel is high speed left wheel is low speed --#
                #high_speed()
                d1 = 192
                #low_speed()
                d2 = 64
                setup_mode(1,0,1)
                pi.set_PWM_dutycycle(Ena1, d1)
                pi.set_PWM_dutycycle(Pha1, d1)
                pi.set_PWM_dutycycle(Ena2, d2)
                pi.set_PWM_dutycycle(Pha2, d2)

                #-- rotate only right wheel --#
                #setup_IN(1,1,1,1)
                #setup_OUT(1,1,0,0)
        
        def turn_right_l(self):
                #-- right wheel is high speed left wheel is low speed --#
                d1 = 128
                d2 = 32
                setup_mode(1,0,1)
                pi.set_PWM_dutycycle(Ena1, d1)
                pi.set_PWM_dutycycle(Pha1, d1)
                pi.set_PWM_dutycycle(Ena2, d2)
                pi.set_PWM_dutycycle(Pha2, d2)

        def turn_left(self):
                #-- right wheel is high speed left wheel is low speed --#
                d1 = 32
                d2 = 128
                setup_mode(1,0,1)
                pi.set_PWM_dutycycle(Ena1, d1)
                pi.set_PWM_dutycycle(Pha1, d1)
                pi.set_PWM_dutycycle(Ena2, d2)
                pi.set_PWM_dutycycle(Pha2, d2)

                #setup_IN(1,1,1,1)
                #setup_OUT(0,0,1,1)

#--- Timer ---#
def timer(t):
        global cond
        time.sleep(t)
        cond = False

#--- Run test ---#
if __name__ == "__main__":
        '''
        try:
                #--- use Timer ---#
                cond = True
                thread = Thread(target = timer,args=([10]))
                thread.start()

                while cond:
                        run = Run()
                        #run. straight_h()
                        run.straight_n()
                time.sleep(1)

        except KeyboardInterrupt:
                run = Run()
                run.stop()
                
        finally:
                run = Run()
                run.stop()
                
        try:
                #--- use Timer ---#
                cond = True
                thread = Thread(target = timer,args=([4]))
                thread.start()

                while cond:
                        run = Run()
                        #run.back()
                        #run.rotation()
                        #run.turn_right()
                        run.turn_right_l()
                        #run.turn_left()
                time.sleep(1)

        except KeyboardInterrupt:
                run = Run()
                run.stop()
                
        finally:
                run = Run()
                run.stop()
        '''
        try:
                start = time.time()
                t = 0
                while t < 10:
                        #--- use Timer ---#
                        global cond
                        cond = True
                        thread = Thread(target = timer,args=([0.5]))
                        thread.start()
                        while cond:
                                run = Run()
                                run.turn_right()
                        time.sleep(0.5)
                        t = time.time() - start

        except KeyboardInterrupt:
                run = Run()
                run.stop()
                
        finally:
                run = Run()
                run.stop()
