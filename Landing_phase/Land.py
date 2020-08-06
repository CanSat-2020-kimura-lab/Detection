import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')

import time
import serial
import pigpio
import BME280
import traceback
import math
import GPS

anypress = 0
Pcount = 0
GAcount = 0
Latestgpsalt = 0
Prevgpsalt = 0
bme280data = []
gpsdata = [0.0, 0.0, 0.0, 0.0, 0.0]
pressdata = [0.0, 0.0, 0.0, 0.0]

def Pressdetect(anypress):
    global bme280data
    global Pcount
    global pressdata
    presslandjudge = 0
    try:
        #print(pressdata)
        Prevpress = pressdata[1]
        #print("Prev=", Prevpress)
        pressdata = BME280.bme280_read()
        Latestpress = pressdata[1]
        #print("Latest=", str(Latestpress))
        deltP = abs(Latestpress - Prevpress)
        #print(str(Latestpress)+"    :    "+str(Prevpress))
        if 0.0 in bme280data:
            print("BME280error!")
            presslandjudge = 2
            Pcount = 0
            #print(Pcount)
        elif deltP < anypress:
            Pcount += 1
            #print(Pcount)
            if Pcount > 4:
                presslandjudge = 1
                print("presslandjudge")
        else:
            Pcount = 0
            #print(Pcount)
    except:
        print(traceback.format_exc())
        Pcount = 0
        presslandjudge = 2
        #print(Pcount)
    return Pcount, presslandjudge

def gpsdetect(anyalt):
    global gpsdata
    global GAcount
    gpslandjudge = 0
    try:
        gpsdata = GPS.readGPS()
        Latestgpsalt = gpsdata[3]
        Prevgpsalt = gpsdata[3]
        daltGA = abs(Latestgpsalt - Prevgpsalt)
        #print(str(Latestgpsslt)+"   :   "+str(Prevgpsalt))
        if daltGA < anyalt:
            GAcount += 1
            if GAcount > 4:
                gpslandjudge = 1
                print("gpslandjudge")
            else:
                gpslandjudge = 0
    except:
        print(traceback.format_exc())
        GAcount = 0
        gpslandjudge = 2
    return GAcount, gpslandjudge

if __name__=="__main__":
    
    print("Start")
    GPS.openGPS()
    BME280.bme280_setup()
    BME280.bme280_calib_param()
    while 1:
        print("Go")
        Pressdetect(0.1)
        time.sleep(1)
    '''
    GPS.openGPS()
    while 1:
        gsplandjudge()
    '''
