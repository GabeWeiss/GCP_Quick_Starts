###
 # Copyright 2018, Google, Inc.
 # Licensed under the Apache License, Version 2.0 (the `License`);
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 # 
 #    http://www.apache.org/licenses/LICENSE-2.0
 # 
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an `AS IS` BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
### 

#!/usr/bin/python

from sense_hat import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import re


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script

ssl_private_key_filepath = '/home/pi/.ssh/ec_private.pem'
ssl_algorithm = 'ES256' # Either RS256 or ES256
root_cert_filepath = '/home/pi/.ssh/roots.pem'
project_id = 'gweiss-demo-project'
gcp_location = 'us-central1'
registry_id = 'demo'
device_id = 'demo'

# end of user-variables

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm) # Assuming RSA, but also supports ECC

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

regExp = re.compile('1')
sense = SenseHat()

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

def message_text(orig):
    print ('matching message text: {}'.format(orig))
    ma = re.match(r'^b\'(.*)\'$', orig)
    return ma.group(1)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

rC = [255,0,0]
oC = [255,69,0]
yC = [255,255,0]
gC = [0,255,0]
bC = [0,0,255]
pC = [128,0,128]
wC = [255,255,255]
blC = [0,0,0]

def respondToMsg(msg):
    if msg == "red":
        sense.clear(255,0,0)
    elif msg == "green":
        sense.clear(0,255,0)
    elif msg == "blue":
        sense.clear(0,0,255)
    elif msg == "rainbow":
        rainbow = [
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC,
        rC, rC, oC, yC, gC, bC, pC, pC
        ]
        sense.set_pixels(rainbow)
    elif msg == "temp":
        sense.show_message(truncate((sense.get_temperature() * (9/5)) + 32, 1))
    else:
        sense.clear()

def on_message(unused_client, unused_userdata, message):
    payload = str(message.payload)
    #print('Received message \'{}\' on topic \'{}\''.format(payload, message.topic))
    respondToMsg(message_text(payload))

def joystick_right(event):
    arrow = [
    blC, blC, blC, blC, wC, blC, blC, blC,
    blC, blC, blC, blC, blC, wC, blC, blC,
    blC, blC, blC, blC, blC, blC, wC, blC,
    wC, wC, wC, wC, wC, wC, wC, wC,
    wC, wC, wC, wC, wC, wC, wC, wC,
    blC, blC, blC, blC, blC, blC, wC, blC,
    blC, blC, blC, blC, blC, wC, blC, blC,
    blC, blC, blC, blC, wC, blC, blC, blC
    ]
    sense.set_pixels(arrow)
def joystick_down(event):
    arrow = [
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    wC, blC, blC, wC, wC, blC, blC, wC,
    blC, wC, blC, wC, wC, blC, wC, blC,
    blC, blC, wC, wC, wC, wC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC
    ]
    sense.set_pixels(arrow)
def joystick_left(event):
    arrow = [
    blC, blC, blC, wC, blC, blC, blC, blC,
    blC, blC, wC, blC, blC, blC, blC, blC,
    blC, wC, blC, blC, blC, blC, blC, blC,
    wC, wC, wC, wC, wC, wC, wC, wC,
    wC, wC, wC, wC, wC, wC, wC, wC,
    blC, wC, blC, blC, blC, blC, blC, blC,
    blC, blC, wC, blC, blC, blC, blC, blC,
    blC, blC, blC, wC, blC, blC, blC, blC
    ]
    sense.set_pixels(arrow)
def joystick_up(event):
    arrow = [
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, wC, wC, wC, wC, blC, blC,
    blC, wC, blC, wC, wC, blC, wC, blC,
    wC, blC, blC, wC, wC, blC, blC, wC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    blC, blC, blC, wC, wC, blC, blC, blC,
    ]
    sense.set_pixels(arrow)
def joystick_press(event):
    sense.clear()

sense.stick.direction_up = joystick_up
sense.stick.direction_down = joystick_down
sense.stick.direction_left = joystick_left
sense.stick.direction_right = joystick_right
sense.stick.direction_middle = joystick_press

client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message

client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
client.connect('mqtt.googleapis.com', 8883)
client.subscribe('/devices/{}/config'.format(device_id), qos=1)
client.loop_start()

# Could set this granularity to whatever we want based on device, monitoring needs, etc
temperature = 0
humidity = 0
pressure = 0

# Send 5 seconds worth of data back up to IoT Core
for i in range(1, 6):
  cur_temp = sense.get_temperature()
  cur_pressure = sense.get_pressure()
  cur_humidity = sense.get_humidity()

  if cur_temp == temperature and cur_humidity == humidity and cur_pressure == pressure:
    time.sleep(1)
    continue

  temperature = cur_temp
  pressure = cur_pressure
  humidity = cur_humidity

  payload = '{{ "ts": {}, "temperature": {}, "pressure": {}, "humidity": {} }}'.format(int(time.time()), temperature, pressure, humidity)
  client.publish(_MQTT_TOPIC, payload, qos=1)

  print("{}\n".format(payload))

  time.sleep(1)

#client.loop_stop()
time.sleep(999)
