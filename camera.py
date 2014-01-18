# Class to put different camera types into a common interface.
# Camera must support:
#  - Calling a readframe function to read the current frame at any time.
#    I.e. could be called sporadically when needed.

import threading
import time

import cv2


CAPTURE_HZ = 30.0


class OpenCVCapture(object):
	def __init__(self, device_id=0):
		# Open the camera.
		self._camera = cv2.VideoCapture(device_id)
		if not self._camera.isOpened():
			self._camera.open()
		# Start a thread to continuously capture frames.
		# This must be done because different layers of buffering
		# in the webcam and OS drivers will cause you to retrieve
		# old frames if they aren't continuously read.
		self._capture_frame = None
		self._capture_lock = threading.Lock()
		self._capture_thread = threading.Thread(target=self._grab_frames)
		self._capture_thread.daemon = True
		self._capture_thread.start()

	def _grab_frames(self):
		while True:
			retval, frame = self._camera.read()
			with self._capture_lock:
				self._capture_frame = None
				if retval:
					self._capture_frame = frame
			time.sleep(1.0/CAPTURE_HZ)

	def read(self):
		frame = None
		with self._capture_lock:
			frame = self._capture_frame
		while frame == None:
			time.sleep(0)
			with self._capture_lock:
				frame = self._capture_frame
		return frame
