# Class to put different camera types into a common interface.
# Camera must support:
#  - Calling a readframe function to read the current frame at any time.
#    I.e. could be called sporadically when needed.

import io
import time

import cv2
import numpy as np
import picamera


class PiCameraCapture(object):
	def __init__(self):
		pass

	def read(self):
		# Create the in-memory stream
		stream = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.capture(stream, format='jpeg')
		# Construct a numpy array from the stream
		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		# "Decode" the image from the array, preserving color
		image = cv2.imdecode(data, 1)
		return image
