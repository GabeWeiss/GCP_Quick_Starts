# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import sys

from google.cloud import iot_v1

#   Variable block. Should be the only pieces needing editing
#
# You shouldn't need to change this variable, it's here for illustration
# purposes. An advantage of calling a Cloud Function within the same project
# is that there are certain environment varibales you get for free like this
# one
project_id  = os.environ['GCP_PROJECT']

# change the following to match your project's values
# you could also easily modify the code to receieve these as variables
# in the GET call since I'm relying on that for the config/command switch
# as well as the actual message being sent
registry_id = '<registry_id>'
gcp_region  = '<project location>'
device_id   = '<device_id>'

# a couple default values for the config messages which will
# reset the LED configurations as a default
incoming_msg   = "clear"  # by default will reset the LED matrix
incoming_which = "config" # by default will send a config message

def update_device(request):
    # If the user passed in a message variable, then update our
    # incoming message to match
    new_config = request.args.get('message')
    final_msg = incoming_msg
    if new_config:
      final_msg = new_config

    binary_data = bytes(final_msg, 'utf-8')
    device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id,
                                                                             gcp_region,
                                                                             registry_id,
                                                                             device_id)

    # If the user passed a which variable, then update config v. command
    new_which = request.args.get('which')
    final_which = incoming_which
    if new_which:
      final_which = new_which

    client = iot_v1.DeviceManagerClient()

    if final_which == "command":
      logging.info("Sending a command")
      client.send_command_to_device(device_name, binary_data)
    elif final_which == "config":
      logging.info("Sending a config")
      client.modify_cloud_to_device_config(device_name, binary_data)
    else:
      return '500'

    # return a success if they had the proper which string because it means
    # it executed the command. We're making a big assumption that it worked
    # but this only returns success that it tried to send it, not whether the
    # device acknolwedged it
    return '200'
