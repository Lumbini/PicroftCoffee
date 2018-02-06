import paho.mqtt.client as mqtt 
import os
import socket
import ssl

def on_connect(client, user, flags, rc):
	print ("Connection returned result: " + str(rc))
	# Subscribing in on_connect() means that if we lose the 
	# connection and reconnect then subscriptions will be renewed.
	client.subscribe("#", 1)


def msg_receive(msg):
	print ("topic: " + msg.topic)
	print ("payload: " + str(msg.payload))

	
def on_message(client, userdata, msg):
	msg_receive(msg)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


aws_host = "a3s6q2w7jgbcoj.iot.us-east-1.amazonaws.com"
aws_port = 8883
client_id = "PicroftCoffee"
thing_name = "PicroftCoffee"
ca_path = "cert/root-CA.crt"
cert_path = "cert/2fde82229d-certificate.pem.crt"
key_path = "cert/2fde82229d-private.pem.key"

mqtt_client.tls_set(ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqtt_client.connect(aws_host, aws_port)

mqtt_client.loop_forever()
