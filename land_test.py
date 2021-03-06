import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Other')

import time
import serial
import pigpio
import BME280
import GPS
import TSL2561
import traceback
import math

anypress = 0
Pcount = 0
GAcount = 0
Mcount = 0
bme280data = []
gpsdata = []

landingLog = '/home/pi/log/landingLog.txt'

t_start = time.time()

def Pressdetect(anypress):
	global bme280data
	global Pcount
	presslandjudge = 0
	try:
		pressdata = BME280.bme280_read()
		Prevpress = pressdata[1]
		Latestpress = pressdata[1]
		deltP = abs(Latestpress - Prevpress)
		print(str(Latestpress)+"    :    "+str(Prevpress))
		if 0.0 in bme280data:
			print("BME280error!")
			presslandjudge = 2
			Pcount = 0
			print(Pcount)
		elif deltP < anypress:
			Pcount += 1
			print(Pcount)
			if Pcount > 4:
				presslandudge = 1
				print("presslandjudge")
		else:
			Pcount = 0
			print(Pcount)
	except:
		print(traceack.format_exc())
		Pcount = 0
		presslandjudge = 2
		print(Pcount)
	return Pcount, presslandjudge

def gpsdetect(anyalt):
	global gpsdata
	global GAcount
	gpslandjudge = 0
	try:
		gpsalt = 0
		gpsdata = GPS.readGPS()
		Latestgpsalt = gpsdata[3]
		Prvevgpalt = gpsdata[3]
		daltGA = abs(latestgpsalt - prevgpsalt)
		print(str(Latestgpsslt)+"	:	"+str(prevgpsalt))
		if daltGA < anyalt
			GAcount += 1
			if GAcount > 4:
				gpslandjuge = 1
				print("gpslandjudge")
			else:
				gpslandjudge = 0
	except:
		print(traceback.format_exc())
		GAcount = 0
		gpslandjudge = 2
	return GAcount, gpslandjudge

if __name__=="_main__":
	print("Landing Phase Started")
	y = 60
	t1 = time.time()
	t2 = t1
	BME280.bme280_setup()
	BME280.bme280_calib_param()
	while (t1 t1-t2<y):
		pressjudge = presslandjudge(0.1)
		time.sleep(1)
		if pressjudge == 1:
			break
		bme280data = BME280.bme280_read()
		Other.saveLog(landLog, time.time() - t_start, Bme.bme280_read())
	print("Land Timeout")
	'''
	GPS.openGPS()
	while 1:
		gsplandjudge()
