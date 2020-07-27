import sys
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/Wireless')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Stuck')

#--- original module ---#
import gps_navigate
import IM920
import BMX055
import GPS
import pwm_control
import Stuck
import Calibration

#--- must be installed module ---#
import pigpio
import numpy as np

#--- default module ---#
import difflib
import time
import traceback
from threading import Thread

GPS_data = [0.0,0.0,0.0,0.0,0.0]

def timer(t):
	global cond
	time.sleep(t)
	cond = False

if __name__ == "__main__":
	#--- difine goal latitude and longitude ---#
	lon2 = 139.5430
	lat2 = 35.553
	#------------- program start -------------#
	direction = Calibration.calculate_direction(lon2,lat2)
	goal_distance = direction["distance"]
	#------------- GPS navigate -------------#
	while goal_distance >= 5:
		#------------- Calibration -------------#
		#--- calculate offset ---#
		magdata = Calibration.magdata_matrix()
		magdata_offset = Calibration.calculate_offset(magdata)
		magx_off = magdata_offset[3]
		magy_off = magdata_offset[4]
		magz_off = magdata_offset[5]
		time.sleep(1)
		#--- calculate θ ---#
		data = Calibration.get_data()
		magx = data[0]
		magy = data[1]
		magz = data[2]
		accx = data[3]
		accy = data[4]
		accz = data[5]
		#--- 0 <= θ <= 360 ---#
		θ = Calibration.calculate_angle_2D(magx,magy,magx_off,magy_off)
		#θ = calculate_angle_3D(accx,accy,accz,magx,magy,magz,magx_off,magy_off,magz_off)
		#------------- rotate contorol -------------#
		Calibration.rotate_control(θ,lon2,lat2)
		location = Stuck.stuck_detection1()
		longitude_past = location[0]
		latitude_past = location[1]

		#------------- run straight -------------#
		for i in range(2):
			try:
				for i in range(2):
					run = pwm_control.Run()
					run.straight_h()
					time.sleep(1)
					#--- Send GPS data ---#
					try:
						while True:
							value = GPS.readGPS()
							latitude_new = value[1]
							longitude_new = value[2]
							print(value)
							print('longitude = '+str(longitude_new))
							print('latitude = '+str(latitude_new))
							time.sleep(1)
							if latitude_new != -1.0 and longitude_new != 0.0 :
								break
					except KeyboardInterrupt:
						GPS.closeGPS()
						print("\r\nKeyboard Intruppted, Serial Closed")

					except:
						GPS.closeGPS()
						print (traceback.format_exc())
					
					IM920.Send(GPS_data)
					#--- calculate  goal direction ---#
					direction = Calibration.calculate_direction(lon2,lat2)
					goal_distance = direction["distance"]
					if goal_distance <= 5:
						break
					#--- 0 <= azimuth <= 360 ---#
					azimuth = direction["azimuth1"]
					#--- calculate θ ---#
					data = Calibration.get_data()
					magx = data[0]
					magy = data[1]
					magz = data[2]
					accx = data[3]
					accy = data[4]
					accz = data[5]
					#--- 0 <= θ <= 360 ---#
					θ = Calibration.calculate_angle_2D(magx,magy,magx_off,magy_off)
					#θ = calculate_angle_3D(accx,accy,accz,magx,magy,magz,magx_off,magy_off,magz_off)

					#--- if rover go wide left, turn right ---#
					#--- 15 <= azimuth <= 360 ---#
					if azimuth - 15 > θ and azimuth - 15 >= 0:
						run = pwm_control.Run()
						run.turn_right()
						time.sleep(0.5)
					#--- 0 <= azimuth < 15 ---#
					elif azimuth - 15 < 0:
						azimuth += 360
						if azimuth - 15 > θ:
							run = pwm_control.Run()
							run.turn_right()
							time.sleep(0.5)							

					#--- if rover go wide right, turn left ---#
					#--- 0 <= azimuth <= 345 ---#
					if θ > azimuth + 15 and  azimuth + 15 > 360:
						run = pwm_control.Run()
						run.turn_left()
						time.sleep(0.5)
					#--- 345 < azimuth <= 360 ---#
					elif azimuth + 15 > 360:
						azimuth -= 360
						if θ > azimuth + 15:
							run = pwm_control.Run()
							run.turn_left()
							time.sleep(0.5)
					#--- stuck detection ---#
					moved_distance = Stuck.stuck_detection2(longitude_past,latitude_past)
					if moved_distance >= 5:
						IM920.Send("rover moved!")
					else:
						#--- stuck escape ---#
						Stuck.stuck_escape()
					
					#--- Send GPS data ---#
					try:
						while True:
							value = GPS.readGPS()
							latitude_new = value[1]
							longitude_new = value[2]
							print(value)
							print('longitude = '+str(longitude_new))
							print('latitude = '+str(latitude_new))
							time.sleep(1)
							if latitude_new != -1.0 and longitude_new != 0.0 :
								break
					except KeyboardInterrupt:
						GPS.closeGPS()
						print("\r\nKeyboard Intruppted, Serial Closed")

					except:
						GPS.closeGPS()
						print (traceback.format_exc())
					
					IM920.Send(GPS_data)
					#--- calculate  goal direction ---#
					direction = Calibration.calculate_direction(lon2,lat2)
					goal_distance = direction["distance"]
					if goal_distance <= 5:
						break
				      
			except KeyboardInterrupt:
				run = pwm_control.Run()
				run.stop()
			
			finally:
				run = pwm_control.Run()
				run.stop()
