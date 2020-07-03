import sys 
sys.psth.append('/home/pi/git/kimuralab/SenseorModuleTest/BME280')
sys.psth.append('/home/pi/git/kimuralab/SenseorModuleTest/BMX055')
sys.psth.append('/home/pi/git/kimuralab/SenseorModuleTest/GPS')
sys.psth.append('/home/pi/git/kimuralab/SenseorModuleTest/Wireless')
sys.psth.append('/home/pi/git/kimuralab/SenseorModuleTest/TSL2561')

import time
import serial
import pigpio 
import BME280
import BMX055
import GPS
import IM920
import math
import traceback

presscount = 0
altcount = 0
Mcount = 0
plcount = 0
bme280data = []
gpsdata = []
bmx055data = []
presslandjudge = 0
gpslandjudge = 0

def pressdetect(anypress):
    global bme280data
    global presscount
    presslandjudge = 0
    try:
        pressdata = BME280.bme280_read()
        prevpress = pressdata[1]
        latestpress = pressdata[1]

        print(str(prevpress)+"    "+str(latestpress))

        deltP = latestpress - prevpress
        if 0.0 in bme280data:
            print("BME280rror!")
            presslandjudge = 2
            presscount = 0
        elif deltP < anypress:
            presscount += 1
            if presscount > 4:
                presslandjudge = 1
                print("presslandjudge")
        else:
            presscount = 0
        print(str(latestpress) + "  :   " + str(prevpress))
    except:
        print(tracebask.format_exc())
        presscount = 0
        presslandjudge = 2
    finally:
        pressreleasejudge = 2
        return pressslandjudge, presscount

def gpsdetect():
    global altcount
    global gpsdata
    gpslandjudge = 0
    prevgpsalt = gpsdata[3] #昨年のGPS.pyでは[utc, lat, lon, sHeight, gHeight]
    latestgpsalt = gpsdata[3]
    gpsdata = GPS.readGPS()
    deltA = latestgpsalt - prevgpsalt
    try:
        prevgpsalt = gpsdata[3]     #昨年のGPS.pyでは[utc, lat, lon, sHeight, gHeight]
        latestgpsalt = gpsdata[3]
        gpsdata = GPS.readGPS()
        deltA = latestgpsalt - prevgpsalt
        if 0.0 in gpsdata:
            print("GPSerror!")
            gpslandjudge = 2
            gpscount = 0
        elif deltA < anygpsalt:
            gpsaltcount += 1
            if gpsaltcount > 4:
                gpslandjudge = 1
                print("gpslandjudge")
        else:
            gpsaltcount = 0
        print(str(latestgpsalt) + " :   " + str(prevgpsalt))
    except:
        print(tracebask.format_exc())
        gpsaltcount = 0
        gpslandjudge = 2
    finally:
        gpslandjudge = 2
        return gpslandjudge, gpsaltcount


if __name__"__main__":
    pressdetect(0)

