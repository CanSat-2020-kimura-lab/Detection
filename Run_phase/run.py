import sys
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/Wireless')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')

#--- original module ---#
import gps_navigate
import IM920
import BMX055
import GPS
import pwm_control
import stuck
import calibration

#--- must be installed module ---#
import picamera
import pigpio
import serial
import numpy as np

#--- default module ---#
import difflib
import time
import traceback
from threading import Thread

def timer(t):
        global cond
        time.sleep(t)
        cond = False

if __name__ == "__main__":
        #--- difine goal latitude and longitude ---#
        lon2 = 139.906
        lat2 = 35.915
        #------------- program start -------------#
        #------------- calibration -------------#
        #--- calculate offset ---#
        magdata = calibration.magdata_matrix()        
        magdata_offset = calibration.calculate_offset(magdata)
        magx_off = magdata_offset[3]
        magy_off = magdata_offset[4]
        magz_off = magdata_offset[5]
        time.sleep(1)
        #--- calculate θ ---#
        data = calibration.get_data()
        magx = data[0]
        magy = data[1]
        magz = data[2]
        accx = data[3]
        accy = data[4]
        accz = data[5]
        θ = calibration.calculate_angle_2D(magx,magy,magx_off,magy_off)
        #θ = calculate_angle_3D(accx,accy,accz,magx,magy,magz,magx_off,magy_off,magz_off)
        #--- rotate contorol ---#
        calibration.rotate_control(θ,lon2,lat2)

        direction = calibration.calculate_direction(lon2,lat2)
        goal_distance = direction["distance"]
        #------------- GPS navigate -------------#
        while goal_distance >= 5:
                location = stuck.stuck_detection1()
                longitude_past = location[0]
                latitude_past = location[1]
                #--- run straight ---#
                #--- use Timer ---#
                global cond
                cond = True
                thread = Thread(target = timer,args=([20]))
                thread.start()

                try:
                        run = pwm_control.Run()
                        run.straight_h()
                
                except KeyboardInterrupt:
                        run = pwm_control.Run()
                        run.stop()

                finally:
                        run = pwm_control.Run()
                        run.stop()
                
                #--- Send GPS data ---#
                GPS.openGPS()
                GPS_data = GPS.readGPS()
                IM920.Send(GPS_data)
                #--- calculate  goal direction ---#
                direction = calibration.calculate_direction(lon2,lat2)
                goal_distance = direction["distance"]
                #--- stuck detection ---#
                moved_distance = stuck.stuck_detection2(longitude_past,latitude_past)
                if moved_distance != 0:
                        pass                                        
                else:
                        #--- stuck escape ---#
                        move_judge = stuck.stuck_confirm()
                        print(move_judge)
                        stuck.stuck_escape(move_judge)
