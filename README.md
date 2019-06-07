** This is not an official Google product **

# Quick start guides

The guides in this repo represent example code given to developers to help jumpstart their adoption of IoT Core in their systems.

### Raspberry Pi basics guide

This is intended as a step by step guide to getting Raspberry Pi up and running sending messages to the Google Cloud Platform using IoT Core. Google Cloud Platform products used: **Cloud IoT Core, Cloud Pub/Sub**
* [01_guide.html](http://htmlpreview.github.com/?https://github.com/GabeWeiss/IoT_Core_Quick_Starts/blob/master/01_guide.html)
  + Step-by-step instructions to follow to get things running.
* [01_basics.py](https://github.com/GabeWeiss/IoT_Core_Quick_Starts/blob/master/01_basics.py)
  + Python code that will be run on device
* [02_basics.py](https://github.com/GabeWeiss/IoT_Core_Quick_Starts/blob/master/02_basics.py)
  + Python code that adds in the code to receive messages from the Cloud and make the sense hat light up with pretty colors.

### Google Cloud Functions

* [02_basics_gcf](https://github.com/GabeWeiss/IoT_Core_Quick_Starts/tree/master/02_basics_gcf)
  + Google Cloud Function for issuing configuration and command messages back down to devices. GET variables provide the message to send, and the switch between config and command. The function in this folder is in Node.js.
* [03_basics_gcf](https://github.com/GabeWeiss/IoT_Core_Quick_Starts/tree/master/03_basics_gcf)
  + Also Google Cloud Functions for issuing configuration and command messages back down to devices. GET variables provide the message to send, and the switch between config and command. These are in Python and Golang.

### Cloud Products used in these tutorials

* [Cloud IoT Core](https://bit.ly/2X6o5HN)
* [Cloud Pub/Sub](https://bit.ly/2M3W96b)
* [Cloud Functions](https://bit.ly/2M8xFZT)
