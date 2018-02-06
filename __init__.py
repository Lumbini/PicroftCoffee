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

from skillFunctions.action import actionFunction

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

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        machine_on_intent = IntentBuilder("MachineOnIntent").\
            require("MachineOnKeyword").build()
        self.register_intent(machine_on_intent, self.handle_machine_on_intent)

        machine_off_intent = IntentBuilder("MachineOffIntent").\
            require("MachineOffKeyword").build()
        self.register_intent(machine_off_intent, self.handle_machine_off_intent)

        action_intent = IntentBuilder("ActionIntent").\
            require("ActionKeyword").build()
        self.register_intent(action_intent, self.handle_action_intent)

        coffee_size_intent = IntentBuilder("CoffeeSizeIntent").\
            require("CoffeeSizeKeyword").build()
        self.register_intent(coffee_size_intent, self.handle_coffee_size_intent)

        coffe_type_intent = IntentBuilder("CoffeeTypeIntent").\
            require("CoffeeTypeKeyword").build()
        self.register_intent(coffe_type_intent, self.handle_coffee_type_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_machine_on_intent(self, message):
        self.speak_dialog("machine.on")
        print (str(message))

    def handle_machine_off_intent(self, message):
        self.speak_dialog("machine.off")

    def handle_action_intent(self, message):
        try:
            action = message.data.get("ActionKeyword").lower()
            actionFunction(action)

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

        self.speak_dialog("The coffee machine will " + action)

    def handle_coffee_size_intent(self, message):
        self.speak_dialog("")

    def handle_coffee_type_intent(self, message):
        self.speak_dialog("")

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