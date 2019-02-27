import base64
import logging
import os
import sys

from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.auth import compute_engine

#   Variable block. Should be the only pieces needing editing
#
#   Note, this is BAD for production, don't do this. The service account
#   private data should be passed into this function so it's encrypted in
#   transit, and so you don't have it static as you may want to change
#   permission levels, etc. For the purposes of this blog demo code, I've
#   done it for ease of calling and to just show what the data looks like.
#   Please please don't do this in production.
service_account_json = <paste contents of the service account json blob here> # Should be a json blob

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

# I'm putting these two variables outside the method only because there may
# be a time that there are multiple versions and rest APIs for IoT Core, and
# I want to be sure that you don't have to dig through the full code to
# find where to modify which API you're talking to
api_version = 'v1'
service_name = 'cloudiotcore'

def get_client():

#   Returns an authorized API client by discovering the IoT API and creating
#   a service object using the service account credentials JSON.
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'

    credentials = service_account.Credentials.from_service_account_info(service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)

def update_device(request):
    # If the user passed in a message variable, then update our
    # incoming message to match
    new_config = request.args.get('message')
    final_msg = incoming_msg
    if new_config:
      final_msg = new_config

    binary_data = base64.urlsafe_b64encode(final_msg.encode('utf-8')).decode('ascii')
    device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id,
                                                                             gcp_region,
                                                                             registry_id,
                                                                             device_id)

    # If the user passed a which variable, then update config v. command
    new_which = request.args.get('which')
    final_which = incoming_which
    if new_which:
      final_which = new_which

    client = get_client()

    if final_which == "command":
      logging.info("Sending a command")
      command_request = {
        "name": device_name,
        "binaryData": binary_data
      }
      return client.projects().locations().registries().devices().sendCommandToDevice(
                                                          name=device_name,
                                                          body=command_request).execute()
    elif final_which == "config":
      config_request = {
        "name": device_name,
        "versionToUpdate": '0',
        "binaryData": binary_data
      }
      logging.info("Sending a config")
      return client.projects().locations().registries().devices().modifyCloudToDeviceConfig(
                                                          name=device_name,
                                                          body=config_request).execute()
    return '500'
