#!/usr/bin/python

import os
import subprocess
from google.cloud import storage
import time

image_dir = "images"
if not os.path.exists(image_dir):
    os.makedirs("images")

cur_time = time.time()
filename = "image_{}.jpg".format(cur_time)
subprocess.run(["fswebcam", "-r 1280x720", "--no-banner", "{}/{}".format(image_dir, filename)])

storage_client = storage.Client()
bucket = storage_client.get_bucket("blog_pi_images")
blob = bucket.blob(filename)
blob.upload_from_filename("./images/{}".format(filename))


