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
        self.initialize_mqtt()

        machine_on_intent = IntentBuilder("MachineOnIntent").\
            require("MachineOnKeyword").require("CoffeeMachineKeyword").build()
        self.register_intent(machine_on_intent, self.handle_machine_on_intent)

        machine_off_intent = IntentBuilder("MachineOffIntent").\
            require("MachineOffKeyword").require("CoffeeMachineKeyword").build()
        self.register_intent(machine_off_intent, self.handle_machine_off_intent)

        action_intent = IntentBuilder("ActionIntent").\
            require("ActionKeyword").optionally("CoffeeSizeKeyword").require("CoffeeTypeKeyword").build()
        self.register_intent(action_intent, self.handle_action_intent)
        
    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def on_connect(self, client, userdata, flags, rc):
        global connect_flag
        connect_flag = True

    def on_message(self, client, userdata, msg):  
        print (msg.topic + " " + str(msg.payload))

    def initialize_mqtt(self):
        self.aws_host = "a3s6q2w7jgbcoj.iot.us-east-1.amazonaws.com"
        self.aws_port = 8883
        self.client_id = "PicroftCoffee"
        self.thing_name = "PicroftCoffee"
        self.ca_path = "/opt/mycroft/skills/PicroftCoffee/cert/root-CA.crt"
        self.cert_path = "/opt/mycroft/skills/PicroftCoffee/cert/2fde82229d-certificate.pem.crt"
        self.key_path = "/opt/mycroft/skills/PicroftCoffee/cert/2fde82229d-private.pem.key"

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.tls_set(self.ca_path, certfile=self.cert_path, keyfile=self.key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        self.mqtt_client.connect(self.aws_host, self.aws_port)
        self.mqtt_client.loop_start()


    def controlFunction(self, control):
        if (control == "off") or (control == "shutdown"):
            # Might be useful to first check if the coffee machine is already off,
            #   or in the middle of brewing. 
            payload = "Power off"
            self.mqtt_client.publish("PicroftCoffee-Control", payload, qos=1)
            self.speak_dialog("machine.off")

        elif (control == "on") or (control == "start"):
            # Send message to turn on coffee
            payload = "Power on"
            self.mqtt_client.publish("PicroftCoffee-Control", payload, qos=1)
            self.speak_dialog("machine.on")

    def actionFunction(self, action, coffeeType):
        if (action == "brew") or (action == "make"):
            # Change state to BREWINGs
            payload = "State brew " + coffeeType
            self.mqtt_client.publish("PicroftCoffee-Control", payload, qos=1)
            
        elif (action == "cancel") or (action == "stop"):
            # Change state to NOT_BUSY
            payload = "State wait " + coffeeType
            self.mqtt_client.publish("PicroftCoffee-Control", payload, qos=1)

    def handle_machine_on_intent(self, message):
        keyword = str(message.data.get("MachineOnKeyword").lower())
        self.controlFunction(keyword)

    def handle_machine_off_intent(self, message):
        keyword = str(message.data.get("MachineOffKeyword").lower())
        self.controlFunction(keyword)

    def handle_action_intent(self, message):
        keyword = str(message.data.get("ActionKeyword").lower())
        coffeeType = str(message.data.get("CoffeeTypeKeyword").lower())
        self.actionFunction(keyword, coffeeType)
        self.speak("The coffee machine will " + keyword + " your " + coffeeType)

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