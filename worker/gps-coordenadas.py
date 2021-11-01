import serial
import time
import string
import pynmea2

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=10)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	# newdata=newdata.decode("utf-8")
	try:
		# print(newdata.decode("utf-8"))
		newdata=newdata.decode("utf-8")
	except:
		pass
	# print(newdata)
	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		lat=newmsg.latitude
		lng=newmsg.longitude
		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
		print("------------")
		print(gps)