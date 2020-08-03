import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Wireless')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
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
#import numpy as np

#--- default module ---#
#import difflib
import time
import traceback
from threading import Thread

GPS_data = [0.0,0.0,0.0,0.0,0.0]

def timer(t):
	global cond
	time.sleep(t)
	cond = False

if __name__ == "__main__":
	BMX055.bmx055_setup()
	GPS.openGPS()
	print('Run Phase Start!')
	#--- difine goal latitude and longitude ---#
	lon2 = 139.9060815
	lat2 = 35.9143235
	#------------- program start -------------#
	direction = Calibration.calculate_direction(lon2,lat2)
	goal_distance = direction["distance"]
	print('goal distance = '+str(goal_distance))
	#------------- GPS navigate -------------#
	while goal_distance >= 15:
		#------------- Calibration -------------#
		print('Calibration Start')
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
		#--- 0 <= θ <= 360 ---#
		θ = Calibration.calculate_angle_2D(magx,magy,magx_off,magy_off)
		#------------- rotate contorol -------------#
		Calibration.rotate_control(θ,lon2,lat2)
		location = Stuck.stuck_detection1()
		longitude_past = location[0]
		latitude_past = location[1]
		#--- initialize count ---#
		loop_count = 0
		stuck_count = 0

		#------------- run straight -------------#
		try:
			if loop_count <= 5:
				print('Go straight')
				run = pwm_control.Run()
				run.straight_h()
				time.sleep(1)
				#--- calculate  goal direction ---#
				direction = Calibration.calculate_direction(lon2,lat2)
				goal_distance = direction["distance"]
				print('goal distance ='+str(goal_distance))
				if goal_distance <= 15:
					break
				#--- 0 <= azimuth <= 360 ---#
				azimuth = direction["azimuth1"]
				#--- calculate θ ---#
				data = Calibration.get_data()
				magx = data[0]
				magy = data[1]
				#--- 0 <= θ <= 360 ---#
				θ = Calibration.calculate_angle_2D(magx,magy,magx_off,magy_off)

				#--- if rover go wide left, turn right ---#
				#--- 15 <= azimuth <= 360 ---#
				if azimuth - 15 > θ and azimuth - 15 >= 0:
					print('turn right to adjustment')
					run = pwm_control.Run()
					run.turn_right_l()
					time.sleep(0.5)
				#--- 0 <= azimuth < 15 ---#
				elif azimuth - 15 < 0:
					azimuth += 360
					if azimuth - 15 > θ:
						print('turn right to adjustment')
						run = pwm_control.Run()
						run.turn_right_l()
						time.sleep(0.5)							

				#--- if rover go wide right, turn left ---#
				#--- 0 <= azimuth <= 345 ---#
				if θ > azimuth + 15 and  azimuth + 15 > 360:
					print('turn left to adjustment')
					run = pwm_control.Run()
					run.turn_left_l()
					time.sleep(0.5)
				#--- 345 < azimuth <= 360 ---#
				elif azimuth + 15 > 360:
					azimuth -= 360
					if θ > azimuth + 15:
						print('turn left to adjustment')
						run = pwm_control.Run()
						run.turn_left_l()
						time.sleep(0.5)
				#--- stuck detection ---#
				moved_distance = Stuck.stuck_detection2(longitude_past,latitude_past)
				if moved_distance >= 5:
					IM920.Send("Rover is moving now")
					print('Rover is moving now')
					stuck_count = 0
				else:
					#--- stuck escape ---#
					IM920.Send("Rover stucks now")
					print('Stuck!')
					Stuck.stuck_escape()
					loop_count -= 1
					stuck_count += 1
					if stuck_count >= 3:
						print("Rover can't move any more")
						break
				#--- calculate  goal direction ---#
				direction = Calibration.calculate_direction(lon2,lat2)
				goal_distance = direction["distance"]
				if goal_distance <= 15:
					break
				loop_count += 1
				print('loop count is '+str(loop_count))

					
		except KeyboardInterrupt:
			run = pwm_control.Run()
			run.stop()
		
		finally:
			run = pwm_control.Run()
			run.stop()
	
	#--- If rover reached 5m from goal, rover will stop ---#
	run = pwm_control.Run()
	run.stop()
