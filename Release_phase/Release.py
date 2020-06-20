import sys  
sys.path.append('/home//pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home//pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home//pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home//pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home//pi/git/kimuralab/SensorModuleTest/TSL2561')

import time
import serial
import pigpio
import BME280
import BMX055
import GPS
import IM920
import TSL2561
improt traceback
#traceback:スタックトレース(エラー発生時に、直前に実行していた関数やメソッドなどの履歴を表示すること)の抽出

luxdata = []
bme280data = []
luxcount = 0
altcount = 0

luxreleasejudge = 0
pressreleasejudge = 0

def luxdetect(anylux):
	global luxdata
	global luxcount
	luxreleasejudge = 0
	try:
		luxdata = TSL2561.readLux()
		
		if luxdata[0]>anylux or luxdata[1]>anylux:
			luxcount += 1
				if luxcount>4:
					luxreleasejudge = 1
					print("luxreleasejudge")
		else:
			luxreleasejudge = 0
			luxcount = 0
	except:
		print(traceback.format_exc())
		luxcount = 0
		luxreleasejudge = 2
	finally:
		luxreleasejudge = 2
		return luxreleasejudge, luxcount

def pressdetect():
	global bme280data
	global altcount
	pressreleasejudge = 0
	try:
		pressdata = BME280.bme280_read()
		latestpress = pressdata[1]
		prevpress = pressdata[1]
		deltA = latestpress - prevpress
		if 0.0 in bme280data:
			print("BME280rror!")
			pressreleasejudge = 2
			altcount = 0
		elif deltA<0:
			altcount += 1
 			pressreleasejudge = 1
			print("pressreleasejudge")
		else:
			altcount = 0
		print(str(latestpress) + "	:	" + str(pressdata[1]))
	except:
		print(tracebask.format_exc())
		altcount = 0
		ltreleasejudge = 2
	finally:
		pressreleasejudge = 2
		return pressreleasejudge, altcount
