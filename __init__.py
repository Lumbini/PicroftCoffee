# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from time import sleep
import paho.mqtt.client as mqtt 
import os
import socket 
import ssl
from random import uniform
import json

# import action
# import machineControl
# import coffeeType
# import coffeeSize

__author__ = 'lumbini'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"



class MachineControlSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(MachineControlSkill, self).__init__(name="MachineControlSkill")
        self.aws_host = None
        self.aws_port = None
        self.thing_name = None
        self.client_id = None
        self.ca_path = None
        self.cert_path = None
        self.key_path = None

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        machine_on_intent = IntentBuilder("MachineOnIntent").\
            require("MachineOnKeyword").require("CoffeeMachineKeyword").build()
        self.register_intent(machine_on_intent, self.handle_machine_on_intent)

        machine_off_intent = IntentBuilder("MachineOffIntent").\
            require("MachineOffKeyword").require("CoffeeMachineKeyword").build()
        self.register_intent(machine_off_intent, self.handle_machine_off_intent)

        action_intent = IntentBuilder("ActionIntent").\
            require("ActionKeyword").optionally("CoffeeSizeKeyword").require("CoffeeTypeKeyword").build()
        self.register_intent(action_intent, self.handle_action_intent)

        # coffee_size_intent = IntentBuilder("CoffeeSizeIntent").\
        #     require("CoffeeSizeKeyword").build()
        # self.register_intent(coffee_size_intent, self.handle_coffee_size_intent)

        # coffe_type_intent = IntentBuilder("CoffeeTypeIntent").\
        #     require("CoffeeTypeKeyword").build()
        # self.register_intent(coffe_type_intent, self.handle_coffee_type_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.

    def initialize_mqtt(self):
        self.aws_host = "a3s6q2w7jgbcoj.iot.us-east-1.amazonaws.com"
        self.aws_port = 8883
        self.client_id = "PicroftCoffee"
        self.thing_name = "PicroftCoffee"
        self.ca_path = "cert/root-CA.crt"
        self.cert_path = "cert/2fde82229d-certificate.pem.crt"
        self.key_path = "cert/2fde82229d-private.pem.key"

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        mqtt_client.tls_set(ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        mqtt_client.connect(aws_host, aws_port)

    def on_connect(client, userdata, flags, rc):
        global connect_flag
        connect_flag = True

    def on_message(client, userdata, msg):  
        print (msg.topic + " " + str(msg.payload))


    def actionFunction(self, action, coffeeType):
        if (action == "brew") or (action == "make"):
            # Change state to BREWING
            # Turn on an LED
            # Publish message over mqtt to turn on LED
            payload = "State BREW " + coffeeType
            mqtt_client.loop_start()
            sleep(0.1)
            mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
            #print ("sent: " + payload)
            mqtt_client.loop_stop()
            
        elif (action == "cancel") or (action == "stop"):
            # Change state to NOT_BUSY
            # Publish message to turn off LED
            payload = "State WAIT " + coffeeType
            mqtt_client.loop_start()
            sleep(0.1)
            mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
            #print ("sent: " + payload)
            mqtt_client.loop_stop()

    def controlFunction(self, keyword):
        if (keyword == "off") or (keyword == "shutdown"):
            # Might be useful to first check if the coffee machine is already off,
            #   or in the middle of brewing. 
            payload = "Power OFF"
            mqtt_client.loop_start()
            sleep(0.1)
            mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
            #print ("sent: " + payload)
            mqtt_client.loop_stop()

        elif (keyword == "on") or (keyword == "start"):
            # Send message to turn on coffee
            payload = "Power ON"
            mqtt_client.loop_start()
            sleep(0.1)
            mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
            #print ("sent: " + payload)
            mqtt_client.loop_stop()

    def handle_machine_on_intent(self, message):
        keyword = message.data.get("MachineOnKeyword")
        self.controlFunction(keyword)
        self.speak_dialog("machine.on")

    def handle_machine_off_intent(self, message):
        keyword = message.data.get("MachineOffKeyword")
        self.controlFunction(keyword)
        self.speak_dialog("machine.off")

    def handle_action_intent(self, message):
        keyword = str(message.data.get("ActionKeyword").lower())
        coffeeType = str(message.data.get("CoffeeTypeKeyword").lower())
        self.actionFunction(keyword, coffeeType)
        self.speak_dialog("The coffee machine will " + keyword + "your " + coffeeType)

    # def handle_coffee_size_intent(self, message):
    #     keyword = message.data.get("CoffeeSizeKeyword")
    #     coffeeSize.coffeeSizeFunction(keyword)
    #     self.speak_dialog("I got the Size")

    # def handle_coffee_type_intent(self, message):
    #     keyword = message.data.get("CoffeeTypeKeyword")
    #     coffeeType.coffeeTypeFunction(keyword)
    #     self.speak_dialog("I got the type")

    # def make_coffee(self, key, value):
    #     coffee[str(key)] = str(value)
    #     print(coffee)



    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return MachineControlSkill()