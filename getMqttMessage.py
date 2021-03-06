import paho.mqtt.client as mqtt
from databases.measurements import *
from subprocess import run

def on_connect(client, userdata, flags, rc):
	print("Connected with result code {0}".format(rc))
	client.subscribe("tempSensor")

def on_message(client, userdata, msg):
	t,h = [float(x) for x in msg.payload.decode("utf-8").split(",")]
	print("{0}*C {1}%".format(t,h))
	addMesurements(t, h)

def photoResistor_connect(client, userdata, flags, rc):
	print("Photo Resistor connected with result code {0}".format(rc))
	client.subscribe("photoSensor")

def photoResistor_message(client, userdata, msg):
	#value = [int(x) for x in msg.payload.decode("utf-8")]
	value = msg.payload.decode("utf-8")
	value = int(value)
	if value >= 300:
		status = "1"
	else:
		status = "0"
	with open("light_status.txt","w") as sfile:
		sfile.write(status)
	print("light: ",value)

def motion_connect(client, userdata, flags, rc):
	print("Motion sensor connected with result code {0}".format(rc))
	client.subscribe("motionSensor")

def motion_message(client, userdata, msg):
	value = msg.payload.decode("utf-8")
	print(value)
	if value == "motion":
		run("go run sendmail/*.go", shell=True)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

photo_clinet = mqtt.Client()
photo_clinet.on_connect = photoResistor_connect
photo_clinet.on_message = photoResistor_message
photo_clinet.connect("localhost", 1883, 60)

motion_client = mqtt.Client()
motion_client.on_connect = motion_connect
motion_client.on_message = motion_message
motion_client.connect("localhost", 1883, 60)

#client.loop_forever()
#photo_clinet.loop_forever()

while True:
	client.loop_start()
	photo_clinet.loop_start()
	motion_client.loop_start()

