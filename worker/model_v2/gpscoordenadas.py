import serial
import time
import string
import pynmea2

def getCoords():
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=10)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	# print(newdata)
	# newdata=newdata.decode("utf-8")
	try:
		# print(newdata.decode("utf-8"))
		newdata=newdata.decode("utf-8")
		# print(newdata)
	except:
		pass
	# print(newdata)
	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		# print(newmsg)
		lat=newmsg.latitude
		lng=newmsg.longitude
		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
		# print("------------")
		# print(gps)
		return lat, lng
	else:
		return 0,0 # temporal para testear que no me estaba agarrando las coordenadas

#while True:
#	print(getCoords())