#!/usr/bin/env python3
import smbus
import errno

def I2CDetect():
	bus_number = 1  # 1 indicates /dev/i2c-1
	bus = smbus.SMBus(bus_number)
	device_count = 0

	i2cModule = []
	for device in range(3, 128):
		try:
			bus.write_byte(device, 0)
			i2cModule.append(hex(device))
			device_count = device_count + 1
		except IOError as e:
			if e.errno != errno.EREMOTEIO:
				print("Error: {0} on address {1}".format(e, hex(address)))
		except Exception as e: # exception if read_byte fails
			print("Error unk: {0} on address {1}".format(e, hex(address)))

	bus.close()
	bus = None
	return i2cModule

if __name__ == "__main__":
	i2cdetect = I2CDetect()
	print(i2cdetect)
