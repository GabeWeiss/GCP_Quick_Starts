import base64
import logging
import os

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
serviceAccount = '<paste contents of the service account json blob here>'

project_id  = os.environ['GCP_PROJECT']
gcp_region  = 'us-central1'
registry_id = 'iot_core_demo'
device_id   = request_json['deviceId']

# a couple default values for the config messages which will
# reset the LED configurations as a default
incoming_msg   = "clear"; // by default will reset the LED matrix
which_msg_type = "config"; // by default will send a config message

# I'm putting these two variables outside the method only because there may
# be a time that there are multiple versions and rest APIs for IoT Core, and
# I want to be sure that you don't have to dig through the full code to
# find where to modify which API you're talking to
api_version = 'v1'
service_name = 'cloudiotcore'

def get_client(service_account_json):

#   Returns an authorized API client by discovering the IoT API and creating
#   a service object using the service account credentials JSON.
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'

    import pdb;pdb.set_trace()
    credentials = compute_engine.Credentials.from_service_account_file(service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)

def update_device(request):
    #request_json = request.get_json(force=True)
    #logging.info(request_json)
    #if not request_json:
    #    return 'We need more details!'

      # TODO: Need to change the new_config over to fetching the GET parameter and
      # changing the msg variable to whatever they sent
    new_config = request.GET.get('message')
    binary_data = base64.urlsafe_b64encode(incoming_msg.encode('utf-8')).decode('ascii')
    device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id,
                                                                             gcp_region,
                                                                             registry_id,
                                                                             device_id)

    client = get_client(service_account)
    if which_msg_type == "command":
      logging.info("Sending a command")
      command_request = {
        "name": device_name,
        "versionToUpdate": '0',
        "binaryData": binary_data
      }
      return client.projects().locations().registries().devices().sendCommandToDevice(
                                                          name=device_name,
                                                          body=command_request).execute()
      )
    elif which_msg_type == "config":
      config_request = {
        "name": device_name,
        "binaryData": binary_data
      }
      logging.info("Sending a config")
      return client.projects().locations().registries().devices().modifyCloudToDeviceConfig(
                                                          name=device_name,
                                                          body=config_request).execute()
    return 0