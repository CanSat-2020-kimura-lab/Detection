import sys
sys.path.append('/home/pi/git/kimuralab/Other')
import picamera
import time
import traceback
import Other

def Capture(path, width = 320, height = 240):
	filepath = ""
	try:
		with picamera.PiCamera() as camera:
			camera.rotation = 270
			camera.resolution = (width,height)	#(width,height)
			filepath = Other.fileName(path,"jpg")
			camera.capture(filepath)
	except picamera.exc.PiCameraMMALError:
		filepath = "Null"
		time.sleep(0.8)
	except:
		print(traceback.format_exc())
		time.sleep(0.1)
		filepath = "Null"
	return filepath

if __name__ == "__main__":
	try:
		for i in range(3):
			photoName = Capture("photo/photo", 160, 120)
			print(photoName)
	except KeyboardInterrupt:
		print('stop')
	except:
		print(traceback.format_exc())
