#!/usr/bin/python

import os
import subprocess
from google.cloud import storage
import time

image_dir = "images"
cur_time = time.time()
filename = "image_{}.jpg".format(cur_time)

image_size = "1280x720"

bucket_name = "blog_pi_images"

if not os.path.exists(image_dir):
    os.makedirs("images")

subprocess.run(["fswebcam", "-r {}".format(image_size), "--no-banner", "{}/{}".format(image_dir, filename)])

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(filename)
blob.upload_from_filename("./{}/{}".format(image_dir, filename))
