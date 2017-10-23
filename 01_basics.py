
/**
 * Copyright 2017, Google, Inc.
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#!/usr/bin/python

from sense_hat import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt

sense = SenseHat()

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': 'gweiss-demo-project'
  }

  with open('/home/pi/.ssh/sensehat_00_private.pem', 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, algorithm='RS256')

_CLIENT_ID = 'projects/gweiss-demo-project/locations/us-central1/registries/sensehat-devices-test/devices/sensehat-00'
_MQTT_TOPIC = '/devices/sensehat-00/events'

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

client.on_connect = on_connect
client.on_publish = on_publish

client.tls_set(ca_certs='/home/pi/.ssh/roots.pem')
client.connect('mqtt.googleapis.com', 8883)
client.loop_start()

# Could set this granularity to whatever we want based on device, monitoring needs, etc
temperature = 0
humidity = 0
pressure = 0

for i in range(1, 11):
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

  #print("{}\n".format(payload))

  time.sleep(1)

client.loop_stop()
